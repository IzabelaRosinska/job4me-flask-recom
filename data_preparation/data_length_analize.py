import math

from file_reader import *
from utils import *

offers = read_json("../files/offers.json")
companies = read_json("../files/companies.json")

# max_val = {}
# for company_name, company in companies.items():
#     val = max_val.setdefault('name', 0)
#     if val < len(company_name):
#         max_val['name'] = len(company_name)
#     for key, text in company.items():
#         val = max_val.setdefault(key, 0)
#         if val < len(company_name):
#             max_val[key] = len(text)
# print(max_val)
#
# # for offer in offers.values():
#
# lengths = {"name": {}, "address": {}, "description": {}}
# for company_name, company in companies.items():
#     lengths['name'].setdefault(str(math.ceil(len(company_name) / 10) * 10), 0)
#     lengths['name'][str(math.ceil(len(company_name) / 10) * 10)] += 1
#     lengths['address'].setdefault(str(math.ceil(len(company['address']) / 10) * 10), 0)
#     lengths['address'][str(math.ceil(len(company['address']) / 10) * 10)] += 1
#     lengths['description'].setdefault(str(math.ceil(len(company['description']) / 100) * 100), 0)
#     lengths['description'][str(math.ceil(len(company['description']) / 100) * 100)] += 1
# print(lengths)


def sort_dict_by_numeric_value(input_dict):
    sorted_items = sorted(input_dict.items(), key=lambda item: int(item[0]))
    sorted_dict = dict(sorted_items)
    return sorted_dict

employees = read_json('../files/employees.json')
lengths = {'email': {}, 'password': {}, 'first_name': {}, 'last_name': {}, 'education_1': {}, 'education_2': {},
           'work_experience_1': {}, 'work_experience_2': {}, 'skills_1': {}, 'skills_2': {}, 'projects_1': {},
           'projects_2': {}, 'about_me': {}, 'hobbies': {}}

for employee in employees.values():
    lengths['email'].setdefault(str(math.ceil(len(employee['email']) / 10) * 10), 0)
    lengths['email'][str(math.ceil(len(employee['email']) / 10) * 10)] += 1
    lengths['password'].setdefault(str(math.ceil(len(employee['password']) / 10) * 10), 0)
    lengths['password'][str(math.ceil(len(employee['password']) / 10) * 10)] += 1
    lengths['first_name'].setdefault(str(math.ceil(len(employee['name'].split(' ')[0]) / 10) * 10), 0)
    lengths['first_name'][str(math.ceil(len(employee['name'].split(' ')[0]) / 10) * 10)] += 1
    lengths['last_name'].setdefault(str(math.ceil(len(employee['name'].split(' ')[1]) / 10) * 10), 0)
    lengths['last_name'][str(math.ceil(len(employee['name'].split(' ')[1]) / 10) * 10)] += 1
    lengths['about_me'].setdefault(str(math.ceil(len(employee['about_me']) / 10) * 10), 0)
    lengths['about_me'][str(math.ceil(len(employee['about_me']) / 10) * 10)] += 1
    lengths['hobbies'].setdefault(str(math.ceil(len(employee['hobbies']) / 10) * 10), 0)
    lengths['hobbies'][str(math.ceil(len(employee['hobbies']) / 10) * 10)] += 1
    lengths['education_1'].setdefault(str(len(employee['education'])), 0)
    lengths['education_1'][str(len(employee['education']))] += 1
    lengths['education_2'].setdefault(str(math.ceil(max([0] + [len(req) for req in employee['education']]) / 10) * 10), 0)
    lengths['education_2'][str(math.ceil(max([0] + [len(req) for req in employee['education']]) / 10) * 10)] += 1
    lengths['work_experience_1'].setdefault(str(len(employee['work_experience'])), 0)
    lengths['work_experience_1'][str(len(employee['work_experience']))] += 1
    lengths['work_experience_2'].setdefault(str(math.ceil(max([0] + [len(req) for req in employee['work_experience']]) / 10) * 10), 0)
    lengths['work_experience_2'][str(math.ceil(max([0] + [len(req) for req in employee['work_experience']]) / 10) * 10)] += 1
    lengths['skills_1'].setdefault(str(len(employee['skills'])), 0)
    lengths['skills_1'][str(len(employee['skills']))] += 1
    lengths['skills_2'].setdefault(str(math.ceil(max([0] + [len(req) for req in employee['skills']]) / 10) * 10), 0)
    lengths['skills_2'][str(math.ceil(max([0] + [len(req) for req in employee['skills']]) / 10) * 10)] += 1
    lengths['projects_1'].setdefault(str(len(employee['projects'])), 0)
    lengths['projects_1'][str(len(employee['projects']))] += 1
    lengths['projects_2'].setdefault(str(math.ceil(max([0] + [len(req) for req in employee['projects']]) / 10) * 10), 0)
    lengths['projects_2'][str(math.ceil(max([0] + [len(req) for req in employee['projects']]) / 10) * 10)] += 1
# print(lengths)

lengths = {'name': {}, 'localizations_1': {}, 'localizations_2': {}, 'requirements_1': {}, 'requirements_2': {}, 'extra_skills_1': {}, 'extra_skills_2': {}, 'duties': {}, 'description': {}}
for offer in offers.values():
    lengths['name'].setdefault(str(math.ceil(len(offer['name']) / 10) * 10), 0)
    lengths['name'][str(math.ceil(len(offer['name']) / 10) * 10)] += 1
    lengths['localizations_1'].setdefault(str(len(offer['localizations'])), 0)
    lengths['localizations_1'][str(len(offer['localizations']))] += 1
    lengths['localizations_2'].setdefault(str(math.ceil(max([0] + [len(req) for req in offer['localizations']]) / 10) * 10), 0)
    lengths['localizations_2'][str(math.ceil(max([0] + [len(req) for req in offer['localizations']]) / 10) * 10)] += 1
    lengths['duties'].setdefault(str(math.ceil(len(offer['duties']) / 100) * 100), 0)
    lengths['duties'][str(math.ceil(len(offer['duties']) / 100) * 100)] += 1
    lengths['description'].setdefault(str(math.ceil(len(offer['description']) / 100) * 100), 0)
    lengths['description'][str(math.ceil(len(offer['description']) / 100) * 100)] += 1
    lengths['requirements_1'].setdefault(str(len(offer['requirements'])), 0)
    lengths['requirements_1'][str(len(offer['requirements']))] += 1
    lengths['requirements_2'].setdefault(str(math.ceil(max([0] + [len(req) for req in offer['requirements']]) / 10) * 10), 0)
    lengths['requirements_2'][str(math.ceil(max([0] + [len(req) for req in offer['requirements']]) / 10) * 10)] += 1
    lengths['extra_skills_1'].setdefault(str(len(offer['extra_skills'])), 0)
    lengths['extra_skills_1'][str(len(offer['extra_skills']))] += 1
    lengths['extra_skills_2'].setdefault(str(math.ceil(max([0] + [len(req) for req in offer['extra_skills']]) / 10) * 10), 0)
    lengths['extra_skills_2'][str(math.ceil(max([0] + [len(req) for req in offer['extra_skills']]) / 10) * 10)] += 1
for key, val in lengths.items():
    print(key)
    print(sort_dict_by_numeric_value(val))
# print(lengths)
# for offer in offers:
#     if offer['level'] == ['Menedźer']:
#         offer['level'] = ['Menedżer']
#
# print(set(data for offer in offers for data in offer['level']))
#
# write_jsonl("files/offers_all.jsonl", offers)

# for offer in offers:
#     if offer['salary']:
#         print(offer['salary'], get_salary_value(offer['salary']))
