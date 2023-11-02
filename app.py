from flask import Flask, jsonify, request

from recommendation import Recommender
from file_reader import *
from request_maps import *
from utils import get_dict_part

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


@app.route('/recommend/<job_fairs_id>/<employee_id>')
def recommend(job_fairs_id, employee_id):
    filter_params = {}
    if loc := request.args.get('loc'):
        filter_params['localizations'] = loc.split(';')
    if forms := request.args.get('forms'):
        filter_params['forms'] = [forms_map[form] for form in forms.split(';') if form in forms_map]
    try:
        if salary := request.args.get('salary'):
            filter_params['salary'] = int(salary)
    except ValueError:
        pass
    if contract_type := request.args.get('contract_types'):
        filter_params['contract_types'] = [contract_types_map[c_t] for c_t in contract_type.split(';') if c_t in
                                           contract_types_map]
    if levels := request.args.get('levels'):
        filter_params['levels'] = [levels_map[level] for level in levels.split(';') if level in levels_map]
    response = []
    try:
        employee = employees[employee_id]
    except Exception:
        return {'error': 'Wrong id'}
    ranking = recommender.get_offers_ranking(employee, filter_params,
                                             get_dict_part(branches_weights, employee['branches']))
    for offer in ranking:
        response.append(offer)
    return jsonify(data=response), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route('/process/<offer_id>')
def process(offer_id):
    if offer_id not in offers_data:
        return {'error': "Wrong id"}
    offer = offers_data[offer_id]
    recommender.load_and_save_offer(offer_id, offer, branches_weights)
    return "Success"
