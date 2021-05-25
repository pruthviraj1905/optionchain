from flask import Flask,render_template
import sqlite3 as sql
from apscheduler.schedulers.background import BackgroundScheduler
import time
from importlib import import_module
import pandas as pd 
import os
import psycopg2
import requests

DATABASE_URL = os.environ.get('DATABASE_URL')

url = 'https://optionscrapy.herokuapp.com/schedule.json'
payload = dict(project='default', spider='live')

app = Flask(__name__)
cron = BackgroundScheduler()
cron.start()

@app.route('/')

def index():
    con = psycopg2.connect(DATABASE_URL) 
    #con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS NIFTY (Time text,Nifty integer,Call_Sum_of_OI integer,Put_Sum_of_OI integer,Diffrence integer)')
    cur.execute("select * from NIFTY")
    con.commit()
   
    rows = cur.fetchall()
    return render_template("list.html",rows = rows)

@cron.scheduled_job('interval', seconds=180)
def scrapper():
    global url,payload
    requests.post(url,data=payload)



if __name__ == '__main__':
    app.run(debug=True)
