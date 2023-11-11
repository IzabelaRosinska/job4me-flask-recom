# import json
#
#
# def read_json(file_path) -> dict:
#     with open(file_path, 'r', encoding='utf-8') as file:
#         return json.load(file)
#
#
# def read_jsonl(file_path) -> list[dict]:
#     with open(file_path, 'r', encoding="utf-8") as file:
#         return [json.loads(row) for row in file]
#
#
# def write_json(file_path, data: dict, indent: int = None):
#     with open(file_path, 'w', encoding='utf-8') as file:
#         json.dump(data, file, ensure_ascii=False, indent=indent)
#
#
# def update_json(file_path, data: dict):
#     old_data = read_json(file_path)
#     old_data.update(data)
#     write_json(file_path, old_data)
#
#
# def write_jsonl(file_path, data: list[dict]):
#     with open(file_path, 'w', encoding='utf-8') as file:
#         for element in data:
#             json.dump(element, file, ensure_ascii=False)
#             file.write('\n')
#
#
# def update_jsonl(file_path, data: list[dict]):
#     with open(file_path, 'a', encoding='utf-8') as file:
#         for element in data:
#             json.dump(element, file, ensure_ascii=False)
#             file.write('\n')
#
#
# def load_embeddings(file_path) -> dict[str, dict]:
#     embeddings = read_json(file_path)
#     return {text_id: {tuple(keys.split('+')): val for keys, val in text_embeddings.items()} for
#             text_id, text_embeddings in embeddings.items()}
#
#
# def load_labels(labels_to_load: list[tuple[str, str, float]]
#                 ) -> tuple[dict[str, dict[str, list[str]]], dict[str, float]]:
#     """
#     loads given labels files
#
#     :param labels_to_load: list of files to load with given branch name, file path and weight for branches labels
#     :return: dictionary with labels maps for branches and dictionary of branches weights
#     """
#     labels_dict = {}
#     labels_weights = {}
#     for branch, file_path, branch_weight in labels_to_load:
#         labels_dict[branch] = read_json(file_path)
#         labels_weights[branch] = branch_weight
#     return labels_dict, labels_weights
#
#
# def get_by_id(file_path, data_id):
#     return read_json(file_path)[data_id]
