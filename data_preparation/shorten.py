
from tqdm import tqdm

from file_reader import *


offers = read_json('../files/offers.json')
companies = read_json('../files/companies.json')


def cut(text, char_limit):
    if len(text) < char_limit:
        return text
    while len(text) > char_limit-1:
        if (index := max(text.rfind("."), text.rfind("\n"), text.rfind(","))) != -1:
            text = text[:index]
        else:
            return ""
    return text + "."


def cut_duties():
    for offer_id, offer in tqdm(offers.items()):
        if len(offer["duties"]) > 1000:
            if text := cut(offer["duties"], 1000):
                offer["duties"] = text
                print(len(text))
            else:
                print(offer["duties"])


def cut_requirements():
    for offer_id, offer in tqdm(offers.items()):
        if len(offer["requirements"]) > 15:
            reqs = [(req, len(req)) for req in offer["requirements"]]
            lengths = sorted([pair[0] for pair in reqs])[:15]
            new_reqs = []
            for req in offer["requirements"]:
                if len(req) in lengths:
                    if new_text := cut(req, 250):
                        new_reqs.append(new_text)
        else:
            new_reqs = []
            for req in offer["requirements"]:
                if new_text := cut(req, 250):
                    new_reqs.append(new_text)
        offer["requirements"] = new_reqs


def check_requirements():
    for offer_id, offer in tqdm(offers.items()):
        if len(offer["requirements"]) > 15:
            for req in offer["requirements"]:
                if len(req) > 250:
                    print(2)
        else:
            for req in offer["requirements"]:
                if len(req) > 250:
                    print(3)


def cut_extra_skills():
    for offer_id, offer in tqdm(offers.items()):
        if len(offer["extra_skills"]) > 10:
            reqs = [(req, len(req)) for req in offer["extra_skills"]]
            lengths = sorted([pair[0] for pair in reqs])[:10]
            new_reqs = []
            for req in offer["extra_skills"]:
                if len(req) in lengths:
                    if new_text := cut(req, 200):
                        new_reqs.append(new_text)
        else:
            new_reqs = []
            for req in offer["extra_skills"]:
                if new_text := cut(req, 200):
                    new_reqs.append(new_text)
        offer["extra_skills"] = new_reqs


def check_extra_skills():
    for offer_id, offer in tqdm(offers.items()):
        if len(offer["extra_skills"]) > 10:
            print(5)
            for req in offer["extra_skills"]:
                if len(req) > 200:
                    print(6)
        else:
            for req in offer["extra_skills"]:
                if len(req) > 200:
                    print(7)


for name, company in companies.items():
    if len(company['description']) > 1000:
        company['description'] = cut(company['description'], 1000)
        print(len(company['description']))
