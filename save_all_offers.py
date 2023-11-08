from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from file_reader import *
from recommendation import Recommender
from utils import get_dict_part


def save_embeddings(input_file, destination_file, sections_to_process: list[list[str]], update: bool = True):
    sentence_transformer = SentenceTransformer('sentence-transformers/LaBSE')
    embeddings = {}
    texts = read_json(input_file)
    for text_id, text in tqdm(texts.items()):
        text_embeddings = {}
        for keys in sections_to_process:
            text_to_process = "\n".join([('\n'.join(text[key]) if isinstance(text[key], list) else text[key])
                                         for key in keys if key in text])
            if text_to_process:
                text_embeddings['+'.join(keys)] =\
                    sentence_transformer.encode(text_to_process, convert_to_tensor=True).tolist()
        embeddings[text_id] = text_embeddings
    update_json(destination_file, embeddings) if update else write_json(destination_file, embeddings)


def save_labels(input_file, recommender: Recommender, branches_weights: dict[str, float], destination_file: str,
                for_offer=True, sum_to_one=True, update: bool = True):
    data = read_json(input_file)
    labels = {text_id: recommender.get_labels(text, for_offer,
                                              get_dict_part(branches_weights, text['branches'] + ['Ogólne', 'Języki']),
                                              sum_to_one) for text_id, text in tqdm(data.items())}
    update_json(destination_file, labels) if update else write_json(destination_file, labels)


labels_data, branches_weights = load_labels([('IT', 'files/labels_IT.json', 3),
                                            ('Sprzedaż', 'files/labels_sprzedaż.json', 2),
                                            ('Zdrowie', 'files/labels_zdrowie.json', 2),
                                            ('Administracja Biura', 'files/labels_AB.json', 2),
                                            ('Ogólne', 'files/labels_soft_skills.json', 1),
                                            ('Języki', 'files/labels_languages.json', 5)])
