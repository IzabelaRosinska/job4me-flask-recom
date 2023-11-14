import os

import pyodbc
from flask import Flask, request, jsonify

from db_connection.db_connect import get_all_offers, get_employee_by_id, get_offer_by_id
from file_reader import load_labels, read_json
from recommendation import Recommender

app = Flask(__name__)

a = '0'
b = '0'
c = '0'
d = '0'
message = ''
try:
    username = os.getenv('AZURE_DB_USER')
    password = os.getenv('AZURE_DB_PASSWORD')
    server = os.getenv('AZURE_DB')
except Exception:
    a = '1'

database = 'miwm'
driver = '{ODBC Driver 17 for SQL Server}'
encrypt = True
try:
    conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver};encrypt'
                          f'=yes')
    cursor = conn.cursor()
except Exception as e:
    b = '1'
    message = str(e)
try:
    labels_data, branches_weights = load_labels([('IT', 'files/labels_IT.json', 3),
                                                 ('Sprzedaż', 'files/labels_sprzedaż.json', 2),
                                                 ('Zdrowie', 'files/labels_zdrowie.json', 2),
                                                 ('Administracja Biura', 'files/labels_AB.json', 2),
                                                 ('Ogólne', 'files/labels_soft_skills.json', 1),
                                                 ('Języki', 'files/labels_languages.json', 5)])

    # offers = read_json('files/offers.json')
    # offers_embeddings = read_json('files/offers_embeddings.json')

    offers, offers_embeddings = get_all_offers(cursor)
except Exception:
    c = '1'

try:
    recommender = Recommender(labels_data)
    recommender.load_offers(offers, branches_weights,
                            embeddings=offers_embeddings)
except Exception:
    d = '1'


@app.route('/')
def index():
    return os.getenv('AZURE_DB_USER') + ' - ' + os.getenv('AZURE_DB_PASSWORD') + ' - ' + os.getenv('AZURE_DB') + \
           ' - Hello! ' + a + b + c + d + ' ' + message


@app.route('/recommend/<job_fairs_id>/<employee_id>', methods=['GET'])
# @api_key_recommend
def recommend(job_fairs_id, employee_id: str):
    filter_params = {}
    if loc := request.args.get('loc'):
        filter_params['localizations'] = loc.split(';')
    if forms := request.args.get('forms'):
        try:
            filter_params['forms'] = [int(form) for form in forms.split(';')]
        except ValueError:
            pass
    if salary := request.args.get('salary'):
        try:
            filter_params['salary'] = int(salary)
        except ValueError:
            pass
    if contract_type := request.args.get('contract_types'):
        try:
            filter_params['contract_types'] = [int(c_t) for c_t in contract_type.split(';')]
        except ValueError:
            pass
    if levels := request.args.get('levels'):
        try:
            filter_params['levels'] = [int(level) for level in levels.split(';')]
        except ValueError:
            pass
    response = []
    try:
        if not (employee := get_employee_by_id(cursor, int(employee_id))):
            return {'error': 'Employee not found'}
    except ValueError:
        return {'error': 'Wrong id'}
    ranking = recommender.get_offers_ranking(employee, filter_params, branches_weights)
    for offer in ranking:
        response.append(offer)
    return jsonify(data=response)


@app.route('/process/<offer_id>', methods=['GET'])
# @api_key_process
def process(offer_id):
    try:
        if not (offer := get_offer_by_id(cursor, int(offer_id))):
            return {'error': 'Offer not found'}
    except ValueError:
        return {'error': 'Wrong id'}
    recommender.load_and_save_offer(offer_id, offer, branches_weights)
    return "Success"
