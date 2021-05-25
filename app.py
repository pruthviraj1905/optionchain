from flask import Flask,render_template
import sqlite3 as sql
from apscheduler.schedulers.background import BackgroundScheduler
import time
from importlib import import_module
import pandas as pd 
import os
import psycopg2
import requests
from psycopg2.extras import DictCursor

DATABASE_URL = os.environ.get('DATABASE_URL')

url = 'https://optionscrapy.herokuapp.com/schedule.json'
payload = dict(project='default', spider='live')

app = Flask(__name__)
cron = BackgroundScheduler()
cron.start()

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
    con = psycopg2.connect(DATABASE_URL)   
    rows = select_rows_dict_cursor("select * from NIFTY")
    return render_template("list.html",rows = rows)

@cron.scheduled_job('interval', seconds=180)
def scrapper():
    global url,payload
    requests.post(url,data=payload)

if __name__ == '__main__':
    app.run(debug=True)
