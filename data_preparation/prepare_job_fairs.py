import random

from data_preparation.fill_companies import get_companies_branches
from file_reader import *


def match_with_organizers():
    job_fairs = read_json('../files/job_fairs.json')
    organizers = read_json('../files/organizers.json')
    organizers_ids = list(organizers.keys())
    print(organizers_ids)
    for job_fair in job_fairs.values():
        job_fair['organizer'] = int(random.choice(organizers_ids))
    write_json('../files/job_fairs.json', job_fairs, 2)


def check_compatible_companies(branches: list[str], companies):
    compatible = []
    for company_id, company in companies.items():
        is_compatible = True
        for branch in company['branches']:
            if branch not in branches:
                is_compatible = False
                break
        if is_compatible:
            compatible.append()


def create_employer_job_fair_matches(max_companies_per_fairs):
    job_fairs = read_json('../files/job_fairs.json')
    employers = read_json('../files/companies.json')
    offers = read_json('../files/offers.json')
    max_val = [49, 71, 7, 39, 51, 49, 71, 55, 49, 71, 49, 51, 49, 49, 39, 7, 49, 49, 55, 51, 7, 39, 49, 71, 55, 49, 71, 51, 7]
    limits = [49, 71, 7, 39, 51, 36, 42, 36, 21, 49, 38, 41, 16, 41, 30, 5, 36, 28, 50, 32, 6, 29, 20, 38, 42, 31, 62, 16, 5]
    accept_rates = [1, 1, 1, 1, 1, 0.9, 0.95, 0.8, 1, 0.6, 1, 0.9, 1, 0.5, 1, 0.75, 1, 0.2, 1, 0.8, 1, 0.9, 0.3, 0.7, 1, 1, 1, 0,4, 0]
    branches_dict, companies_branches = get_companies_branches(employers, offers, True)
    connections = []
    for (job_fair_id, job_fair), limit, accept in zip(job_fairs.items(), limits, accept_rates):
        branches = set(job_fair['branches'])
        compatible = [name for name, company_branches in companies_branches.items() if company_branches & branches]
        print(job_fair['branches'])
        print(len(compatible))
        choice = random.choices(compatible, k=min(limit, len(compatible)))
        connections += [[job_fair_id, 0 if random.uniform(0, 1) > accept else 1, company] for company in choice]
    write_json('../files/job_fairs_employers_connection.json', connections)


create_employer_job_fair_matches(30)







# match_with_organizers()
