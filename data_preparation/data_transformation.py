import json

from tqdm import tqdm

levels_map = {
    "specialist (Mid / Regular), junior specialist (Junior)": ["Junior", "Mid"],
    "junior specialist (Junior)": ["Junior"],
    "specjalista (Mid / Regular), młodszy specjalista (Junior)": ["Junior", "Mid"],
    "młodszy specjalista (Junior)": ["Junior"],
    "asystent, młodszy specjalista (Junior)": ["Stażysta", "Junior"],
    "specialist (Mid / Regular)": ["Mid"],
    "specjalista (Mid / Regular), starszy specjalista (Senior)": ["Mid", "Senior"],
    "specjalista (Mid / Regular)": ["Mid"],
    "specialist (Mid / Regular), senior specialist (Senior)": ["Mid", "Senior"],
    "senior specialist (Senior), expert": ["Senior"],
    "starszy specjalista (Senior)": ["Senior"],
    "senior specialist (Senior)": ["Senior"],
    "starszy specjalista (Senior), ekspert": ["Senior"],
    "trainee": ["Stażysta"],
    "praktykant / stażysta": ["Stażysta"],
    "kierownik / koordynator, menedżer": ["Menedżer"],
    "manager / supervisor, team manager": ["Menedżer"],
    "team manager": ["Menedżer"],
    "menedżer": ["Menedźer"],
    "kierownik / koordynator": ["Menedżer"],
    "asystent": ["Junior"],
    "manager / supervisor": ["Menedżer"],
    "ekspert": ["Senior"],
    "assistant, junior specialist (Junior)": ["Junior"],
    "pracownik fizyczny": [],
    "assistant": ['Junior'],
    "dyrektor, menedżer": ["Menedżer"],
    "director": ["Menedżer"],
    "dyrektor": ["Menedżer"]
}

forms_map = {
    'hybrid work': ["praca hybrydowa"],
    'praca stacjonarna, praca zdalna, praca hybrydowa': ["praca stacjonarna", "praca hybrydowa", "praca zdalna"],
    'praca zdalna': ["praca zdalna"],
    'praca hybrydowa': ["praca hybrydowa"],
    'praca stacjonarna, praca hybrydowa': ["praca stacjonarna", "praca hybrydowa"],
    'full office work, home office work, hybrid work': ["praca stacjonarna", "praca hybrydowa", "praca zdalna"],
    'home office work': ["praca zdalna"],
    'praca zdalna, praca hybrydowa': ["praca hybrydowa", "praca zdalna"],
    'praca stacjonarna': ["praca stacjonarna"],
    'full office work': ["praca stacjonarna"],
    'home office work, hybrid work': ["praca hybrydowa", "praca zdalna"],
    'praca mobilna': ["praca zdalna"],
    'full office work, hybrid work': ["praca hybrydowa", "praca zdalna"],
    'mobile work': ["praca zdalna"]
}

contract_types_map = {
    'contract of employment, B2B contract': ["umowa o pracę", "kontrakt B2B"],
    'contract of employment': ["umowa o pracę"],
    'umowa o pracę': ["umowa o pracę"],
    'kontrakt B2B': ["kontrakt B2B"],
    'umowa o pracę, kontrakt B2B': ["umowa o pracę", "kontrakt B2B"],
    'umowa o pracę, umowa zlecenie, kontrakt B2B, umowa o pracę tymczasową': ["umowa o pracę", "umowa zlecenie", "kontrakt B2B"],
    'umowa o pracę, umowa zlecenie, kontrakt B2B': ["umowa o pracę", "umowa zlecenie", "kontrakt B2B"],
    'umowa o pracę, umowa zlecenie': ["umowa o pracę", "umowa zlecenie"],
    'contract of mandate': ["umowa zlecenie"],
    'umowa o pracę, umowa o staż / praktyki': ["umowa o staż", "umowa o pracę"],
    'B2B contract': ["kontrakt B2B"],
    'contract of employment, agency agreement': ["umowa o pracę"],
    'substitution agreement': ["umowa zlecenie"],
    'umowa zlecenie, kontrakt B2B': ["umowa zlecenie", "kontrakt B2B"],
    'contract of mandate, B2B contract': ["umowa zlecenie", "kontrakt B2B"],
    'umowa zlecenie': ["umowa zlecenie"],
    'contract of employment, contract of mandate': ["umowa o pracę", "umowa zlecenie"],
    'umowa o dzieło, umowa zlecenie, umowa o staż / praktyki': ["umowa o staż", "umowa zlecenie"],
    'umowa na zastępstwo': ["umowa zlecenie"],
    'kontrakt B2B, umowa na zastępstwo': ["umowa zlecenie", "kontrakt B2B"],
    'umowa o staż / praktyki': ["umowa o staż"],
    'internship / apprenticeship contract': ["umowa o staż"],
    'temporary staffing agreement': ["umowa zlecenie"],
    'contract of employment, contract of mandate, B2B contract': ["umowa o pracę", "umowa zlecenie", "kontrakt B2B"],
    'umowa o dzieło, umowa zlecenie, kontrakt B2B': ["umowa zlecenie", "kontrakt B2B"],
    'umowa o dzieło, umowa zlecenie': ["umowa zlecenie"],
    'umowa o pracę tymczasową': ['umowa o pracę'],
    'umowa o pracę, umowa o dzieło, umowa zlecenie, kontrakt B2B': ["umowa o pracę", "umowa zlecenie", "kontrakt B2B"],
    'umowa zlecenie, kontrakt B2B, umowa agencyjna': ["umowa zlecenie", "kontrakt B2B"],
    'umowa o pracę, umowa na zastępstwo': ["umowa o pracę"],
    'umowa o dzieło, kontrakt B2B': ["kontrakt B2B"],
    'umowa o pracę, umowa o dzieło': ["umowa o pracę"],
    'umowa o pracę, umowa o dzieło, umowa zlecenie': ["umowa o pracę", "umowa zlecenie"]
}

working_times_map = {
    'full-time': "pełny etat",
    'pełny etat': "pełny etat",
    'pełny etat, część etatu': "pełny etat",
    'full-time, part time': "pełny etat",
    'część etatu': "część etatu",
    'additional / temporary': "część etatu",
    'część etatu, dodatkowa / tymczasowa': "część etatu",
    'part time': "część etatu",
    'pełny etat, część etatu, dodatkowa / tymczasowa': "pełny etat",
    'pełny etat, dodatkowa / tymczasowa': 'pełny etat',
    'dodatkowa / tymczasowa': "część etatu"
}


def check_data(data):
    results = {key: {} for key in data[0]}
    for offer in data:
        for key, val in offer.items():
            if isinstance(val, list):
                if len(val) in results[key]:
                    results[key][len(val)] += 1
                else:
                    results[key][len(val)] = 1
            elif val:
                if True in results[key]:
                    results[key][True] += 1
                else:
                    results[key][True] = 1
            elif False in results[key]:
                results[key][False] += 1
            else:
                results[key[False]] = 1
    return results


def get_description(about_project, what_we_offer, char_limit=500):
    if not about_project:
        while len(what_we_offer) > char_limit:
            what_we_offer = what_we_offer[:-1]
            if (index := what_we_offer.rfind(".")) != -1:
                what_we_offer = what_we_offer[:index + 1]
            else:
                return ""
        return what_we_offer
    if len(what_we_offer) + len(about_project) + 2 < char_limit:
        return about_project + '\n\n' + what_we_offer
    while len(about_project) > char_limit:
        about_project = about_project[:-1]
        if (index := about_project.rfind(".")) != -1:
            about_project = about_project[:index + 1]
        else:
            while len(what_we_offer) > char_limit:
                what_we_offer = what_we_offer[:-1]
                if (index := what_we_offer.rfind(".")) != -1:
                    what_we_offer = what_we_offer[:index + 1]
                else:
                    return ""
    return about_project


def transform_data(data: list[dict], category):
    with open('companies_all.json', 'r', encoding='utf-8') as file:
        companies = json.load(file)
    offers_new = []
    for offer in tqdm(data):
        new_offer = {'name': offer['name'], 'company': offer['company'], 'branches': [category],
                     'localizations': [offer['localization'][0].split(", ")[-1]], 'forms': forms_map[offer['form']],
                     'salary': offer['salary'], 'contract_type': contract_types_map[offer['contract_type']],
                     'working_time': working_times_map[offer['working_time']], 'level': levels_map[offer['level']],
                     'requirements': offer['requirements'], 'extra_skills': offer['extra_skills'],
                     'duties': offer['duties'],
                     'description': get_description(offer['about_project'], offer['what_we_offer'])}
        for localization in offer['localization'][1:]:
            localization = localization[0].split(", ")[-1]
            if localization not in new_offer['localizations']:
                new_offer['localizations'].append(localization)

        if offer['company'] not in companies:
            companies[offer['company']] = {"contact_email": "", "contact_phone": "",
                                           "address": offer['localization'][0], "description": offer['about_us']}
        offers_new.append(new_offer)
    with open('offers_all.jsonl', 'a', encoding='utf-8') as file:
        for element in offers_new:
            json.dump(element, file, ensure_ascii=False)
            file.write('\n')
    with open('companies_all.json', 'w', encoding='utf-8') as file:
        json.dump(companies, file, ensure_ascii=False)


with open('offers_administracja_biurowa.jsonl', 'r', encoding='utf-8') as file:
    offers = [json.loads(offer) for offer in file]

transform_data(offers, "Administracja Biurowa")
