from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
import sqlite3 
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp

from helpers import login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# SQLite3 database 
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

@app.route('/')
@login_required
def index():
    userID = session['id']
    
    # Get settings
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        settings = cursor.execute('SELECT nhl, nba, nfl, mlb FROM settings WHERE id = ?', (userID,))
        conn.commit()
    
    settings = settings.fetchall()
    # Store each individual setting in dict
    sports = {
        'nhl': settings[0]['nhl'],
        'nba': settings[0]['nba'],
        'nfl': settings[0]['nfl'],
        'mlb': settings[0]['mlb']
    }
    return render_template('index.html', sports=sports)

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
        with sqlite3.connect('database.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute('SELECT * FROM users WHERE username = ?',
                                (username,))
            conn.commit()
        
        rows = rows.fetchall()
        # Check for valid username/password
        if not rows or not check_password_hash(rows[0]['hash'], password):
            session['error'] = 'Invalid username and/or password'
            return redirect('error.html')

        # Store user ID in session
        session['id'] = rows[0]['id']

        return redirect('/')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
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
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            takenUsers = cursor.execute('SELECT username FROM users')
            conn.commit()

        # Compare each username to make sure no duplicates
        if newUser in takenUsers:
            session['error'] = 'Username already taken'
            return redirect('/error')

        # Insert new username and hash into db
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, hash) VALUES (?, ?)',
                            (newUser, generate_password_hash(newPassword)))

            # Get user ID and store in session
            session['id'] = cursor.lastrowid
            cursor.execute('INSERT INTO settings (id) VALUES (?)', (session['id'],))

            conn.commit()

        return redirect('/')
    else:
        return render_template('signup.html')

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    id = session['id']
    if request.method == 'POST':
        newNHL = request.form.get('nhl')
        newNBA = request.form.get('nba')
        newNFL = request.form.get('nfl')
        newMLB = request.form.get('mlb')

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            # Check each sport for new setting
            if newNHL == 'off':
                cursor.execute('UPDATE settings SET nhl = 0 WHERE id = ?', (id,))
            else:
                cursor.execute('UPDATE settings SET nhl = 1 WHERE id = ?', (id,))

            if newNBA == 'off':
                cursor.execute('UDPATE settings SET nba = 0 WHERE id = ?', (id,))
            else:
                cursor.execute('UPDATE settings SET nba = 1 WHERE id = ?', (id,))

            if newNFL == 'off':
                cursor.execute('UDPATE settings SET nfl = 0 WHERE id = ?', (id,))
            else:
                cursor.execute('UPDATE settings SET nfl = 1 WHERE id = ?', (id,))

            if newMLB == 'off':
                cursor.execute('UDPATE settings SET mlb = 0 WHERE id = ?', (id,))
            else:
                cursor.execute('UPDATE settings SET mlb = 1 WHERE id = ?', (id,))

            conn.commit()

        return render_template('/')
    else:
        # Check current settings
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            currentSettings = cursor.execute('SELECT nhl, nba, nfl, mlb FROM settings WHERE id = ?',
                                            (id,))
            conn.commit()
        # Render settings with previous settings
        nhl = currentSettings[0]['nhl']
        nba = currentSettings[0]['nba']
        nfl = currentSettings[0]['nfl']
        mlb = currentSettings[0]['mlb']

        return render_template('settings.html', nhl=nhl, nba=nba, nfl=nfl, mlb=mlb)


@app.route('/error', methods=['GET', 'POST'])
def error():
    # Render error template with error message
    return render_template('error.html', error_message=session['error'])

if __name__ == '__main__':
    app.secret_key = '\xb0\xc732\x04\x08\xf9\x11\x13\xdf\xd6\xba\x94&\xdf3\xa3I\xdfG\xc7\xc0\xc7\xaa'
    app.run()