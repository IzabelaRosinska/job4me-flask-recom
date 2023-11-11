# import re
#
#
# def delete_ending(word: str):
#     rules = [
#         (r'(em|am|o|eś|aś|e|ka)$', ''),
#         (r'(asz|ał|ął|any|ani)$', "ać"),
#         (r'(dzie)$', 'd'),
#         (r'(s|es|ed|ing|er|ist)$', ''),
#         (r'(om|ów|ami|ę|a|e|y|i|iej|ou|u|ach|ych)$', ''),
#         (r'(ow|czny|i)$', ''),
#         (r'(yjn)$', 'j'),
#         (r'(-,\')$', '')
#     ]
#     for rule, replacement in rules:
#         if len(word) > 3:
#             word = re.sub(rule, replacement, word)
#         else:
#             return word
#     return word
#
#
# def tokenize(text: str, text_only: bool = False) -> list[str]:
#     if text_only:
#         return re.sub(r'[^\w\s]', '', text).split()
#     pattern = re.compile(r'\w+|[.,!?;()]')
#     return pattern.findall(text)
#
#
# def lemmatize(text: str, text_only: bool = False) -> list[str]:
#     return [delete_ending(word) for word in tokenize(text, text_only)]
#
#
# def check_words_similarity(word1, word2) -> bool:
#     return delete_ending(word1) == delete_ending(word2)
#
#
# def find_next(word, tree):
#     for node in tree:
#         if check_words_similarity(word, node):
#             return node
#     return None
#
#
# def get_salary_value(salary: str, as_month_salary=True) -> list[int]:
#     if not salary:
#         return []
#     salary_range = salary.replace(',', '.').replace(' zł', '').split('–')
#     try:
#         salary_range = [float(val) for val in salary_range[:2]]
#         return [int(val * 160 if as_month_salary and val < 1000 else val) for val in salary_range]
#     except ValueError:
#         return []
#
#
# def check_list_filter_param(offer_value: list, filter_value: set) -> bool:
#     if filter_value:
#         for val in offer_value:
#             if val in filter_value:
#                 return True
#         return False
#     return True
#
#
# def check_salary(offer_salary: str, filter_salary: int | None) -> bool:
#     if filter_salary:
#         if value := get_salary_value(offer_salary):
#             return value[0] >= filter_salary
#         return False
#     return True
#
#
# def filter_offers(offers: dict[dict[str | list[str]]], filter_params: dict) -> list:
#     if not filter_params:
#         return list(offers.keys())
#     accepted = []
#     localizations = set(filter_params['localizations']) if 'localizations' in filter_params else set()
#     level = set(filter_params['levels']) if 'levels' in filter_params else set()
#     salary = filter_params['salary'] if 'salary' in filter_params else None
#     forms = set(filter_params['forms']) if 'forms' in filter_params else set()
#     contract_type = set(filter_params['contract_types']) if 'contract_types' in filter_params else set()
#     for offer_id, offer in offers.items():
#         if check_list_filter_param(offer['localizations'], localizations) and check_list_filter_param(
#                 offer['levels'], level) and check_list_filter_param(
#                 offer['forms'], forms) and check_salary(offer['min_salary'], salary) and check_list_filter_param(
#                 offer['contract_types'], contract_type):
#             accepted.append(offer_id)
#     return accepted
#
#
# def get_dict_part(dictionary: dict, keys_to_get: list[str]) -> dict:
#     return {key: dictionary[key] for key in keys_to_get if key in dictionary}
