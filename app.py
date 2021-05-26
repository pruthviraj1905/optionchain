from flask import Flask,render_template
import time
from importlib import import_module
import pandas as pd 
import os
import psycopg2
import requests
from psycopg2.extras import DictCursor

DATABASE_URL = os.environ.get('DATABASE_URL')

app = Flask(__name__)


def select_rows_dict_cursor(query):
    """Run SELECT query and return list of dicts."""
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(query)
        records = cur.fetchall()
    cur.close()
    return records

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nifty')
def nifty():
    con = psycopg2.connect(DATABASE_URL)   
    rows = select_rows_dict_cursor("select * from NIFTY ORDER BY Time DESC")
    return render_template("nifty.html",rows = rows)

@app.route('/banknifty')
def banknifty():
    con = psycopg2.connect(DATABASE_URL)   
    rows = select_rows_dict_cursor("select * from BANKNIFTY ORDER BY Time DESC")
    return render_template("banknifty.html",rows = rows)


if __name__ == '__main__':
    app.run(debug=True)