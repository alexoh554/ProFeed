from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
import sqlite3 
from werkzeug.security import check_password_hash, generate_password_hash

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

@app.route('/signup')
def signup():
    if request.method == 'POST':
        # Check for correct input
        newUser = request.form.get('username')
        newPassword = request.form.get('password')

        if len(newUser) < 4 or len(newUser) > 12:
            session['error'] = 'Username must be between 4 - 16 characters'
            return redirect('/error')
        if len(newPassword) < 6 or len(newPassword) > 16:
            session['error'] = 'Password must be between 6 - 16 Characters'
            return redirect('/error')
        # Check if password matches confirm
        if newPassword != request.form.get('confirmation'):
            session['error'] = 'Passwords do not match'
            return redirect('/error')

        # Store all taken usernames
        takenUsers = []
        takenUsers = cursor.execute('SELECT username FROM users')

        # Compare each username to make sure no duplicates
        if newUser in takenUsers:
            session['error'] = 'Username already taken'
            return redirect('/error')

        # Insert new username and hash into db
        cursor.execute('INSERT INTO users (username, hash) VALUES (:username, :password)',
                        username=newUser, password=generate_password_hash(newPassword))
        
        # Get user ID and store in session
        tmp = cursor.execute('SELECT * FROM users WHERE username = :username',
                            username=newUser)
        session['id'] = tmp[0]['id']
        
        return redirect('/')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'POST':
        # Check if user input username/password
        if not request.form.get('username'):
            session['error'] = 'Must input a username'
            return redirect('error.html')
        if not request.form.get('password'):
            session['error'] = 'Must input a password'
            return redirect('error.html')

        username = request.form.get('username')
        password = request.form.get('password')

        # Query database into rows
        rows = cursor.execute('SELECT * FROM users WHERE username = :username',
                                username=username)

        # Check for valid username/password
        if len(rows) != 1 or not check_password_hash(rows[0]['hash'], password):
            session['error'] = 'Invalid username and/or password'
            return redirect('error.html')

        # Store user ID in session
        session['id'] = rows[0]['id']

        return redirect('/')
    else:
        return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():


@app.route('/error', methods=['GET', 'POST'])
def error():
    # Render error template with error message
    return render_template('error.html', error_message=session['error'])