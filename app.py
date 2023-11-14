import os

import pyodbc
from flask import Flask

from file_reader import load_labels, read_json

app = Flask(__name__)


a = '0'
b = '0'
c = '0'
try:
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
except Exception:
    username = "miwm"
    password = "job4meZPI"
    a = '1'
server = "tcp:miwmjob4me.database.windows.net,1433"
database = 'miwm'
driver = '{ODBC Driver 17 for SQL Server}'
try:
    conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')
    cursor = conn.cursor()
except Exception:
    b = '1'

try:
    labels_data, branches_weights = load_labels([('IT', 'files/labels_IT.json', 3),
                                                 ('Sprzedaż', 'files/labels_sprzedaż.json', 2),
                                                 ('Zdrowie', 'files/labels_zdrowie.json', 2),
                                                 ('Administracja Biura', 'files/labels_AB.json', 2),
                                                 ('Ogólne', 'files/labels_soft_skills.json', 1),
                                                 ('Języki', 'files/labels_languages.json', 5)])

    offers = read_json('files/offers.json')
    offers_embeddings = read_json('files/offers_embeddings.json')
except Exception:
    c = '1'


# recommender = Recommender(cursor, labels_data)
# recommender.load_offers(offers, branches_weights,
#                         labels=read_json("files/offers_labels.json"),
#                         embeddings=offers_embeddings)
@app.route('/')
def index():
    return 'Hello! ' + a + b + c
