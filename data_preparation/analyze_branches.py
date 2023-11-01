from tqdm import tqdm

from file_reader import *
from recommendation import Recommender

labels_data, branches_weights = load_labels([('IT', '../files/labels_IT.json', 1),
                                             ('Sprzedaż', '../files/labels_sprzedaż.json', 1),
                                             ('Zdrowie', '../files/labels_zdrowie.json', 1),
                                             ('Administracja Biura', '../files/labels_AB.json', 1)])


offers = read_json('../files/offers.json')

recommender = Recommender("../files/offers_labels_saved.json", "../files/offers_embeddings_saved.json", labels_data)

new_offers = {}

for offer_id, offer in tqdm(offers.items()):
    recognized = {branch: recommender.get_labels(offer, True, {branch: weight}, False) for branch, weight in
                  branches_weights.items()}
    branches = [branch for branch in branches_weights if
                sum([val for key, val in recognized[branch].items() if key not in ['trener', 'rekrutacja']]) >= 15]
    if branches:
        offer["branches"] = branches
        new_offers[offer_id] = offer

write_json('../files/offers.json', new_offers)
