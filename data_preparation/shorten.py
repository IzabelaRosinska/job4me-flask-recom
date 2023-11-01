import random

from tqdm import tqdm

from file_reader import *


# offers = read_json('../files/offers.json')
companies = read_json('../files/companies.json')


def cut(text, char_limit):
    if len(text) < char_limit:
        return text
    while len(text) > char_limit-1:
        # text = text[:-1]
        if (index := max(text.rfind("."), text.rfind("\n"), text.rfind(","))) != -1:
            text = text[:index]
        else:
            return ""
    return text + "."


# new_offers = {}
# for offer_id, offer in tqdm(offers.items()):
#     if len(offer["duties"]) > 1000:
#         if text := cut(offer["duties"], 1000):
#             offer["duties"] = text
#             print(len(text))
#         else:
#             print(offer["duties"])
#             print(1)

# new_offers = {}
# for offer_id, offer in tqdm(offers.items()):
#     if len(offer["requirements"]) > 15:
#         reqs = [(req, len(req)) for req in offer["requirements"]]
#         lengths = sorted([pair[0] for pair in reqs])[:15]
#         new_reqs = []
#         for req in offer["requirements"]:
#             if len(req) in lengths:
#                 if new_text := cut(req, 250):
#                     if len(new_text) > 250:
#                         print(1)
#                     new_reqs.append(new_text)
#                 # print(len(new_reqs[-1]))
#     else:
#         new_reqs = []
#         for req in offer["requirements"]:
#             if new_text := cut(req, 250):
#                 if len(new_text) > 250:
#                     print(2)
#                 new_reqs.append(new_text)
#             # print(len(new_reqs[-1]))
#     offer["requirements"] = new_reqs
#
# new_offers = {}
# for offer_id, offer in tqdm(offers.items()):
#     # print(len(offer["requirements"]))
#     if len(offer["requirements"]) > 15:
#         print(1)
#         reqs = [(req, len(req)) for req in offer["requirements"]]
#         lengths = sorted([pair[0] for pair in reqs])[:15]
#         for req in offer["requirements"]:
#             if len(req) > 250:
#                 print(2)
#     else:
#         new_reqs = []
#         for req in offer["requirements"]:
#             if len(req) > 250:
#                 print(3)


# new_offers = {}
# for offer_id, offer in tqdm(offers.items()):
#     if len(offer["extra_skills"]) > 10:
#         reqs = [(req, len(req)) for req in offer["extra_skills"]]
#         lengths = sorted([pair[0] for pair in reqs])[:10]
#         new_reqs = []
#         for req in offer["extra_skills"]:
#             if len(req) in lengths:
#                 if new_text := cut(req, 200):
#                     if len(new_text) > 200:
#                         print(3)
#                     new_reqs.append(new_text)
#                 # print(len(new_reqs[-1]))
#     else:
#         new_reqs = []
#         for req in offer["extra_skills"]:
#             if new_text := cut(req, 200):
#                 if len(new_text) > 200:
#                     print(4)
#                 new_reqs.append(new_text)
#             # print(len(new_reqs[-1]))
#     offer["extra_skills"] = new_reqs

# new_offers = {}
# for offer_id, offer in tqdm(offers.items()):
#     # print(len(offer["requirements"]))
#     if len(offer["extra_skills"]) > 10:
#         print(5)
#         reqs = [(req, len(req)) for req in offer["extra_skills"]]
#         lengths = sorted([pair[0] for pair in reqs])[:10]
#         for req in offer["extra_skills"]:
#             if len(req) > 200:
#                 print(6)
#     else:
#         new_reqs = []
#         for req in offer["extra_skills"]:
#             if len(req) > 200:
#                 print(7)


# write_json('../files/offers.json', offers)

for name, company in companies.items():
    if len(company['description']) > 1000:
        company['description'] = cut(company['description'], 1000)
        print(len(company['description']))

# write_json('../files/companies.json', companies)