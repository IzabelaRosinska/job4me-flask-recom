import os

import pyodbc
from flask import Flask

app = Flask(__name__)


a = '0'
b = '0'
try:
    server = os.getenv('DB_SERVER')
except Exception:
    server = "tcp:miwmjob4me.database.windows.net,1433"
    a = '1'
database = 'miwm'
username = "miwm"
password = "job4meZPI"
driver = '{ODBC Driver 17 for SQL Server}'
try:
    conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')
except Exception:
    b = '1'


@app.route('/')
def index():
    return 'Hello! ' + a + b
