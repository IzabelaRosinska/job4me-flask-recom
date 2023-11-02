from flask import Flask, jsonify

from recommendation import Recommender
from file_reader import *

app = Flask(__name__)


labels_data, branches_weights = load_labels([('IT', 'files/labels_IT.json', 3),
                                             ('Sprzedaż', 'files/labels_sprzedaż.json', 2),
                                             ('Zdrowie', 'files/labels_zdrowie.json', 2),
                                             ('Administracja Biura', 'files/labels_AB.json', 2),
                                             ('Ogólne', 'files/labels_soft_skills.json', 1),
                                             ('Języki', 'files/labels_languages.json', 5)])


offers_data = read_json("files/offers.json")

recommender = Recommender("files/offers_labels_saved.json", "files/offers_embeddings_saved.json", labels_data)
recommender.load_offers_from_db(offers_data, branches_weights,
                                labels=read_json("files/offers_labels.json"),
                                embeddings=load_embeddings("files/offers_embeddings.json"))
employees = read_json('files/employees.json')


@app.route('/')
def index():
    return 'Hello!'


@app.route('/recommend/<employee_id>')
def recommend(employee_id):
    response = []
    employee = employees[employee_id]
    ranking = recommender.get_offers_ranking(employee, branches_weights)
    for offer in ranking:
        response.append(offer)
    return jsonify(data=response), 200, {'Content-Type': 'application/json; charset=utf-8'}
