from matching.matcher import Labels_Matcher
from utils.utils import filter_offers, cosine_similarity


class Recommender:
    def __init__(self, labels: dict[str, dict[str, list[str]]] = None, matcher: Labels_Matcher = None,
                 weights_cv: dict[str, float] = None, weights_offers: dict[str, float] = None,
                 cos_sim_correlations: list[tuple[str, str, float]] = None, branches_weights: dict[str, float] = None):

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
            self.weights_cv = {"education": 2, "experience": 1000, "projects": 100,
                               "skills": 5, "about_me": 2, "hobbies": 1}
        if weights_offers:
            self.weights_offers = weights_offers
        else:
            self.weights_offers = {"name": 2000, "requirements": 50, "extra_skills": 5, "duties": 2, "description": 1}
        if branches_weights:
            self.branches_weights = branches_weights
        else:
            self.branches_weights = {'IT': 3, 'Sprzedaż': 2, 'Zdrowie': 2, 'Administracja Biura': 2,
                                     'Ogólne': 1, 'Języki': 5}
        self.offers_filter_params = {}
        self.offers_labels = {}
        self.offers_embeddings = {}
        self.employees_labels = {}
        self.employees_embeddings = {}

    def get_labels(self, data: dict[str, str | list[str]], for_offer: bool, sum_to_one: bool = True
                   ) -> dict[str, float]:
        labels = {}
        for sector, sector_weight in (self.weights_offers.items() if for_offer else self.weights_cv.items()):
            if sector_weight != 0 and sector in data:
                recognized_labels = self.labels_matcher.match(('\n'.join(data[sector]) if isinstance(data[sector], list)
                                                               else data[sector]), list(self.branches_weights.keys()))
                for branch, branch_labels in recognized_labels.items():
                    branch_weight = self.branches_weights[branch]
                    for label in branch_labels:
                        labels.setdefault(label, 0)
                        labels[label] += sector_weight * branch_weight
        if sum_to_one:
            sum_of_weights = sum(labels.values())
            return {label: weight / sum_of_weights for label, weight in labels.items()}
        return labels

    def extract_filter_params_from_offer(self, offer_id, offer):
        offer_filter_params = {'localizations': offer['localizations'] if 'localization' in offer else [],
                               'min_salary': offer['min_salary'] if 'min_salary' in offer else None,
                               'levels': offer['levels'] if 'levels' in offer else [],
                               'branches': offer['branches'] if 'branches' in offer else [],
                               'company': offer['company'] if 'company' in offer else None,
                               'contract_types': offer['contract_types'] if 'contract_types' in offer else [],
                               'forms': offer['forms'] if 'forms' in offer else []}
        self.offers_filter_params[offer_id] = offer_filter_params

    def load_offers(self, offers: dict[str, dict], embeddings: dict[str, dict],
                    labels: dict[str, dict[str, float]] = None):
        for offer_id, offer in offers.items():
            self.extract_filter_params_from_offer(offer_id, offer)
        self.offers_embeddings.update(embeddings)
        if labels:
            self.offers_labels.update(labels)
        else:
            for offer_id, offer in offers.items():
                self.offers_labels[offer_id] = self.get_labels(offer, True)

    def load_employees(self, employees: dict[str, dict], embeddings: dict[str, dict],
                       labels: dict[str, dict[str, float]] = None):
        self.employees_embeddings.update(embeddings)
        if labels:
            self.employees_labels.update(labels)
        else:
            for employee_id, employee in employees.items():
                self.employees_labels[employee_id] = self.get_labels(employee, False)

    def update_offer_labels(self, offer_id, offer: dict):
        self.extract_filter_params_from_offer(offer_id, offer)
        self.offers_labels[offer_id] = self.get_labels(offer, True)

    def update_offers_embeddings(self, offers_embeddings: dict):
        self.offers_embeddings.update(offers_embeddings)

    def update_employee_labels(self, employee_id, employee: dict):
        self.offers_labels[employee_id] = self.get_labels(employee, True)

    def update_employees_embeddings(self, employees_embeddings: dict):
        self.employees_embeddings.update(employees_embeddings)

    def remove_offer(self, offer_id: int):
        if offer_id in self.offers_filter_params:
            del self.offers_filter_params[offer_id]
        if offer_id in self.offers_labels:
            del self.offers_labels[offer_id]
        if offer_id in self.offers_embeddings:
            del self.offers_embeddings[offer_id]

    def remove_employee(self, employee_id):
        if employee_id in self.employees_labels:
            del self.employees_labels[employee_id]
        if employee_id in self.employees_labels:
            del self.employees_labels[employee_id]

    @staticmethod
    def get_labels_sim(employee_labels: dict[str, float], offer_labels: dict[str, float]) -> float:
        score = 0
        shared = set(employee_labels.keys()) & set(offer_labels.keys())
        for label in shared:
            score += (min(employee_labels[label], offer_labels[label]) * 10) ** 2
        for label in (set(offer_labels.keys()) - shared):
            score -= (offer_labels[label] * 5) ** 2
        return score

    def get_cos_sim(self, employee_embeddings, offer_embeddings) -> float:
        score = 0
        total_weight = 0
        for employee_key, offer_key, weight in self.cos_sim_correlations:
            if employee_key in employee_embeddings and offer_key in offer_embeddings and weight != 0:
                score += cosine_similarity(employee_embeddings[employee_key],
                                           offer_embeddings[offer_key]).item() * weight
            total_weight += weight
        return score / total_weight if total_weight != 0 else 0

    def get_offers_ranking(self, employee_id, employers_on_job_fairs, filter_params: dict,
                           number_to_pass_to_embeddings=20, embeddings_weight=5) -> list[int] | dict:
        if employee_id not in self.employees_labels:
            return {'error': 'Employee not found'}
        employee_labels = self.employees_labels[employee_id]
        ranking = [(offer_id, self.get_labels_sim(employee_labels, self.offers_labels[offer_id]))
                   for offer_id in filter_offers(self.offers_filter_params, employers_on_job_fairs, filter_params)]
        ranking = sorted(ranking, key=lambda x: x[1], reverse=True)
        if employee_id in self.employees_embeddings and (employee_embeddings := self.employees_embeddings[employee_id]):
            new_ranking = []
            for offer, score in ranking[:number_to_pass_to_embeddings]:
                if self.offers_embeddings[offer]:
                    new_ranking.append((offer, score + embeddings_weight *
                                        self.get_cos_sim(employee_embeddings, self.offers_embeddings[offer])))
            new_ranking = sorted(new_ranking, key=lambda x: x[1], reverse=True)
            return [ranking_position[0] for ranking_position in new_ranking + ranking[number_to_pass_to_embeddings:]]
        return [ranking_position[0] for ranking_position in ranking]
