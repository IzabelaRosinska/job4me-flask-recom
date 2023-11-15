from sentence_transformers import util

from matcher import Labels_Matcher
from db_connection.db_connect import *
from utils import filter_offers


class Recommender:
    def __init__(self, cursor: pyodbc.Cursor,
                 labels: dict[str, dict[str, list[str]]] = None, matcher: Labels_Matcher = None,
                 weights_cv: dict[str, float] = None, weights_offers: dict[str, float] = None,
                 cos_sim_correlations: list[tuple[str, str, float]] = None):

        self.cursor = cursor
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

    def load_offers(self, offers: dict[str, dict[str, str | list[str]]], branches_weights: dict[str, float],
                    embeddings: dict[str, dict], labels: dict[str, dict[str, float]] = None):
        self.offers.update(offers)
        for offer_id, offer in offers.items():
            self.offers_labels[offer_id] = (labels[offer_id] if labels and offer_id in labels else
                                            self.get_labels(offer, True, branches_weights))
            self.offers_embeddings[offer_id] = embeddings[offer_id]

    def load_and_save_offer(self, offer_id: str, offer: dict[str, str | list[str]], branches_weights: dict[str, float]):
        self.offers[offer_id] = offer
        self.offers_labels[offer_id] = self.get_labels(offer, True, branches_weights)

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
            if employee_key in employee_embeddings and offer_key in offer_embeddings and weight != 0:
                score += util.pytorch_cos_sim(employee_embeddings[employee_key],
                                              offer_embeddings[offer_key]).item() * weight
                total_weight += weight
        return score / total_weight if total_weight != 0 else 0

    def get_offers_ranking(self, employee_data: dict[str, str | list[str]], filter_params: dict,
                           branches_weights: dict[str, float]) -> list[dict[str, str | list[str]]]:
        employee_labels = self.get_labels(employee_data, False, branches_weights)
        ranking = [(offer_id, self.get_labels_sim(employee_labels, self.offers_labels[offer_id]))
                   for offer_id in filter_offers(self.offers, filter_params)]
        ranking = sorted(ranking, key=lambda x: x[1], reverse=True)
        return [ranking_position[0] for ranking_position in ranking]
