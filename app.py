from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
import sqlite3 

from helpers import login_required

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# SQLite3 database 
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

@app.route('/')
@login_required
def index():
    # home page

    #display news feed chosen by user
    return True
