import random

from file_reader import *
from utils import get_salary_value

offers = read_json('../files/offers.json')


def get_salaries_ranges(offers):
    salaries = {}
    for offer in offers.values():
        if offer['salary']:
            print(offer['salary'])
            salary = get_salary_value(offer['salary'])
            for level in offer['level']:
                for branch in offer['branches']:
                    val = salaries.setdefault((level, branch), [0, 0, 0, 0])
                    salaries[(level, branch)] = [val[0] + salary[0], val[1] + (salary[1] if len(salary) > 1 else 0), val[2] + 1, val[3] + (1 if len(salary) > 1 else 0)]
    salaries_norm = {cat: (round(a / c), round(b / d)) for cat, (a, b, c, d) in salaries.items()}
    salaries_ranges = {cat: (round(a * 0.007), round(a * 0.013), round(b * 0.007), round(b * 0.013)) for cat, (a, b) in salaries_norm.items()}
    return salaries_ranges


def fill_salaries(offers, salaries_ranges):
    new_offers = {}
    for offer_id, offer in offers.items():
        new_offer = {"name": offer['name'], 'company': offer['company'], 'branches': offer['branches'], 'localizations': offer['localizations'], 'forms': offer['forms'], 'contract_types': offer['contract_type'], 'working_time': offer['working_time'], 'levels': offer['level']}
        if offer['salary']:
            salary = get_salary_value(offer['salary'], False)
            new_offer['payment_frequency'] = 'month' if salary[0] > 1000 else 'hour'
            new_offer['min_salary'] = salary[0]
            if len(salary) > 1:
                new_offer['max_salary'] = salary[1]
        else:
            min_min_salary = None
            max_min_salary = None
            min_max_salary = None
            max_max_salary = None
            for level in offer['level']:
                for branch in offer['branches']:
                    if (level, branch) in salaries_ranges:
                        min_min_s, max_min_s, min_max_s, max_max_s = salaries_ranges[(level, branch)]
                        if not min_min_salary or min_min_salary > min_min_s:
                            min_min_salary = min_min_s
                        if not max_min_salary or max_min_salary < max_min_s:
                            max_min_salary = max_min_s
                        if not min_max_salary or min_max_salary > min_max_s:
                            min_max_salary = min_max_s
                        if not max_max_salary or max_max_salary < max_max_s:
                            max_max_salary = max_max_s

            min_salary = 50
            max_salary = 0
            if min_min_salary and max_min_salary:
                min_salary = random.randint(min_min_salary, max_min_salary)
            if min_max_salary and max_max_salary:
                max_salary = random.randint(min_max_salary, max_max_salary)
            new_offer['payment_frequency'] = 'month'
            new_offer['min_salary'] = min_salary
            if min_salary < max_salary:
                new_offer['max_salary'] = max_salary
        new_offer['requirements'] = offer['requirements']
        new_offer['extra_skills'] = offer['extra_skills']
        new_offer['duties'] = offer['duties']
        new_offer['description'] = offer['description']
        new_offers[offer_id] = new_offer
    return new_offers


write_json('../files/offers.json', fill_salaries(offers, get_salaries_ranges(offers)))


