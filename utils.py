import re


def delete_ending(word: str):
    rules = [
        (r'(em|am|o|eś|aś|e|ka)$', ''),
        (r'(asz|ał|ął|any|ani)$', "ać"),
        (r'(dzie)$', 'd'),
        (r'(s|es|ed|ing|er|ist)$', ''),
        (r'(om|ów|ami|ę|a|e|y|i|iej|ou|u|ach|ych)$', ''),
        (r'(ow|czny|i)$', ''),
        (r'(yjn)$', 'j'),
        (r'(-,\')$', '')
    ]
    for rule, replacement in rules:
        if len(word) > 3:
            word = re.sub(rule, replacement, word)
        else:
            return word
    return word


def check_words_similarity(word1, word2) -> bool:
    return delete_ending(word1) == delete_ending(word2)


def find_next(word, tree):
    for node in tree:
        if check_words_similarity(word, node):
            return node
    return None


def get_salary_value(salary: str, as_month_salary=True) -> list[int]:
    if not salary:
        return []
    salary_range = salary.replace(',', '.').replace(' zł', '').split('–')
    try:
        salary_range = [float(val) for val in salary_range[:2]]
        return [int(val * 160 if as_month_salary and val < 1000 else val) for val in salary_range]
    except ValueError:
        return []


def check_list_filter_param(offer_value: list, filter_value: set) -> bool:
    if filter_value:
        for val in offer_value:
            if val in filter_value:
                return True
        return False
    return True


def check_salary(offer_salary: str, filter_salary: int | None) -> bool:
    if filter_salary:
        if value := get_salary_value(offer_salary):
            return value[0] >= filter_salary
        return False
    return True


def get_dict_part(dictionary: dict, keys_to_get: list[str]) -> dict:
    return {key: dictionary[key] for key in keys_to_get if key in dictionary}
