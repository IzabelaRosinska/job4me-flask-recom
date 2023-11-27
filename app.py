import os

from flask import Flask, request, jsonify

from connection.db_connect import *
from utils.file_reader import load_labels
from matching.recommendation import Recommender
from connection.api_authentication import *

app = Flask(__name__)

username = os.getenv('AZURE_DB_USER')
password = os.getenv('AZURE_DB_PASSWORD')
server = os.getenv('AZURE_DB')
database = 'miwm'
driver = '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')
cursor = conn.cursor()

labels_data, branches_weights = load_labels([('IT', 'files/labels_IT.json', 3),
                                             ('Sprzedaż', 'files/labels_sprzedaż.json', 2),
                                             ('Zdrowie', 'files/labels_zdrowie.json', 2),
                                             ('Administracja Biura', 'files/labels_AB.json', 2),
                                             ('Ogólne', 'files/labels_soft_skills.json', 1),
                                             ('Języki', 'files/labels_languages.json', 5)])

offers, offers_embeddings = get_filtered_offers(cursor, 'a')
employees, employees_embeddings = get_all_employees(cursor)

recommender = Recommender(labels=labels_data, branches_weights=branches_weights)
recommender.load_offers(offers, offers_embeddings)
recommender.load_employees(employees, employees_embeddings)

conn.close()


@app.route('/')
def index():
    return 'choose service'


@app.route('/recommend/<job_fairs_id>/<employee_id>', methods=['GET'])
@api_key_recommend
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
    try:
        employee_id = int(employee_id)
    except ValueError:
        return {'error': 'Wrong employee id'}
    try:
        job_fairs_id = int(job_fairs_id)
    except ValueError:
        return {'error': 'Wrong job fair id'}

    conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')
    cursor = conn.cursor()
    employers_on_job_fairs = get_employers_on_job_fairs(cursor, job_fairs_id)
    conn.close()

    response = recommender.get_offers_ranking(employee_id, employers_on_job_fairs, filter_params)
    return response


@app.route('/update-offer/<offer_id>', methods=['GET'])
@api_key_update_offer
def update_offer(offer_id):
    try:
        offer_id = int(offer_id)
    except ValueError:
        return {'error': 'Wrong id'}
    conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')
    cursor = conn.cursor()
    if not (offer := get_offer_by_id(cursor, offer_id)):
        return {'error': 'Offer not found'}
    conn.close()
    recommender.update_offer_labels(offer_id, offer)
    return "Offer labels updated successfully"


@app.route('/update-offers-embeddings', methods=['GET'])
@api_key_update_offers_embeddings
def update_offers_embeddings():
    conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')
    cursor = conn.cursor()
    embeddings = get_offers_embeddings_only(cursor)
    conn.close()
    recommender.update_offers_embeddings(embeddings)
    return "Offers embeddings updated successfully"


@app.route('/update-employee/<employee_id>', methods=['GET'])
@api_key_update_employee
def update_employee(employee_id):
    try:
        employee_id = int(employee_id)
    except ValueError:
        return {'error': 'Wrong id'}
    conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')
    cursor = conn.cursor()
    if not (employee := get_offer_by_id(cursor, employee_id)):
        return {'error': 'Employee not found'}
    conn.close()
    recommender.update_employee_labels(employee_id, employee)
    return "Employee labels updated successfully"


@app.route('/update-employees-embeddings', methods=['GET'])
@api_key_update_employees_embeddings
def update_employees_embeddings():
    conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')
    cursor = conn.cursor()
    embeddings = get_employees_embeddings_only(cursor)
    conn.close()
    recommender.update_employees_embeddings(embeddings)
    return "Employees embeddings updated successfully"


@app.route('/remove-offer/<offer_id>', methods=['GET'])
@api_key_remove_offer
def remove_offer(offer_id):
    try:
        offer_id = int(offer_id)
    except ValueError:
        return {'error': 'Wrong id'}
    conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')
    cursor = conn.cursor()
    if check_if_offer_is_disabled(cursor, offer_id):
        conn.close()
        recommender.remove_offer(offer_id)
        return 'Offer removed from service memory'
    else:
        conn.close()
        return {'error': 'Offer is still active'}


@app.route('/remove-employee/<employee_id>', methods=['GET'])
@api_key_remove_employee
def remove_employee(employee_id):
    try:
        employee_id = int(employee_id)
    except ValueError:
        return {'error': 'Wrong id'}
    conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')
    cursor = conn.cursor()
    if check_if_employee_is_deleted(cursor, employee_id):
        conn.close()
        recommender.remove_employee(employee_id)
        return 'Emloyee removed from service memory'
    else:
        conn.close()
        return {'error': 'Employee is still in database'}

