from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import logging

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

SEARCH_QUEUE_FILE = "../search_queue.txt"

def parse_search_queue():
    entries = []
    current_entry = {}
    if not os.path.exists(SEARCH_QUEUE_FILE):
        return entries

    with open(SEARCH_QUEUE_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                if current_entry:
                    entries.append(current_entry)
                    current_entry = {}
                continue
            if ": " in line:
                key, value = line.split(": ", 1)
                current_entry[key] = value
    if current_entry:
        entries.append(current_entry)
    return entries

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    entries = parse_search_queue()
    return render_template('dashboard.html', entries=entries, username=session.get('username'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
