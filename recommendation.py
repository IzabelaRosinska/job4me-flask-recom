from sentence_transformers import SentenceTransformer, util
from matcher import Labels_Matcher
from utils import filter_offers
from file_reader import *


class Recommender:
    def __init__(self, labels_file: str, embeddings_file: str,
                 labels: dict[str, dict[str, list[str]]] = None, matcher: Labels_Matcher = None,
                 weights_cv: dict[str, float] = None, weights_offers: dict[str, float] = None,
                 cos_sim_correlations: list[tuple[str, str, float]] = None):

        self.labels_file = labels_file
        self.embeddings_file = embeddings_file

        if cos_sim_correlations:
            self.cos_sim_correlations = cos_sim_correlations
        else:
            self.cos_sim_correlations = [('work_experience+projects', "duties", 20),
                                         ("about_me+hobbies", "description", 1),
                                         ("skills", "requirements+extra_skills", 5)]
        if matcher:
            self.labels_matcher = matcher
        elif labels:
            self.labels_matcher = Labels_Matcher(labels)
        else:
            raise AttributeError("Labels list or matcher not provided - cannot initialize labels matcher")
        if weights_cv:
            self.weights_cv = weights_cv
        else:
            self.weights_cv = {"education": 2, "work_experience": 50, "projects": 50,
                               "skills": 5, "about_me": 2, "hobbies": 1}
        if weights_offers:
            self.weights_offers = weights_offers
        else:
            self.weights_offers = {"name": 100, "requirements": 20, "extra_skills": 5, "duties": 2, "description": 1}
        self.offers = {}
        self.offers_labels = {}
        self.offers_embeddings = {}
        self.sentence_transformer = SentenceTransformer('sentence-transformers/LaBSE')

    def get_labels(self, data: dict[str, str | list[str]], for_offer: bool, branches_weights: dict[str, float],
                   sum_to_one: bool = True) -> dict[str, float]:
        labels = {}
        for sector, sector_weight in (self.weights_offers.items() if for_offer else self.weights_cv.items()):
            if sector_weight != 0 and sector in data:
                recognized_labels = self.labels_matcher.match(('\n'.join(data[sector]) if isinstance(data[sector], list)
                                                               else data[sector]), list(branches_weights.keys()))
                for branch, branch_labels in recognized_labels.items():
                    branch_weight = branches_weights[branch]
                    for label in branch_labels:
                        labels.setdefault(label, 0)
                        labels[label] += sector_weight * branch_weight
        if sum_to_one:
            sum_of_weights = sum(labels.values())
            return {label: weight / sum_of_weights for label, weight in labels.items()}
        return labels

    def get_embeddings(self, data: dict[str, str | list[str]], for_offer: bool):
        embeddings = {}
        if for_offer:
            for _, keys, _ in self.cos_sim_correlations:
                text = "\n".join([('\n'.join(data[key]) if isinstance(data[key], list) else data[key])
                                  for key in keys.split('+') if key in data])
                if text:
                    embeddings[keys] = self.sentence_transformer.encode(text, convert_to_tensor=True).tolist()
        else:
            for keys, _, _ in self.cos_sim_correlations:
                text = "\n".join([('\n'.join(data[key]) if isinstance(data[key], list) else data[key])
                                  for key in keys.split('+') if key in data])
                if text:
                    embeddings[keys] = self.sentence_transformer.encode(text, convert_to_tensor=True)
        return embeddings

    def load_offers_from_db(self, offers: dict[str, dict[str, str | list[str]]], branches_weights: dict[str, float],
                            labels: dict[str, dict[str, float]] = None, embeddings: dict[str, dict] = None):
        self.offers.update(offers)
        for offer_id, offer in offers.items():
            self.offers_labels[offer_id] = (labels[offer_id] if labels and offer_id in labels else
                                            self.get_labels(offer, True, branches_weights))
            self.offers_embeddings[offer_id] = (embeddings[offer_id] if embeddings and offer_id in embeddings else
                                                self.get_embeddings(offer, True))

    def load_and_save_offer(self, offer_id: str, offer: dict[str, str | list[str]], branches_weights: dict[str, float]):
        self.offers[offer_id] = offer
        self.offers_labels[offer_id] = self.get_labels(offer, True, branches_weights)
        self.offers_embeddings[offer_id] = self.get_embeddings(offer, True)
        update_json(self.labels_file, {offer_id: self.offers_labels[offer_id]})
        update_json(self.embeddings_file, {offer_id: self.offers_embeddings[offer_id]})

    @staticmethod
    def get_labels_sim(employee_labels: dict[str, float], offer_labels: dict[str, float]) -> float:
        score = 0
        shared = set(employee_labels.keys()) & set(offer_labels.keys())
        for label in shared:
            score += (cur_sim := min(employee_labels[label], offer_labels[label]))
        return score

    def get_cos_sim(self, employee_embeddings, offer_embeddings) -> float:
        score = 0
        total_weight = 0
        for employee_key, offer_key, weight in self.cos_sim_correlations:
            if tuple(employee_key) in employee_embeddings and tuple(offer_key) in offer_embeddings and weight != 0:
                score += util.pytorch_cos_sim(employee_embeddings[tuple(employee_key)],
                                              offer_embeddings[tuple(offer_key)]).item() * weight
                total_weight += weight
        return score / total_weight if total_weight != 0 else 0

    def get_offers_ranking(self, employee_data: dict[str, str | list[str]],
                           branches_weights: dict[str, float]) -> list[dict[str, str | list[str]]]:
        employee_labels = self.get_labels(employee_data, False, branches_weights)
        employee_embeddings = self.get_embeddings(employee_data, False)
        ranking = [(offer_id, self.get_labels_sim(employee_labels, self.offers_labels[offer_id]))
                   for offer_id in self.offers]
        ranking = sorted(ranking, key=lambda x: x[1], reverse=True)
        new_ranking = []
        for offer, score in ranking[:100]:
            new_ranking.append((offer, score + self.get_cos_sim(employee_embeddings, self.offers_embeddings[offer])))
        new_ranking = sorted(new_ranking, key=lambda x: x[1], reverse=True)
        return [ranking_position[0] for ranking_position in new_ranking + ranking[100:]]
