from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

# DATABASE
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# LOGIN PAGE
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect('/dashboard')
        else:
            error = "Invalid Username or Password"

    return render_template('login.html', error=error)


# REGISTER
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except:
        return "❌ Username already exists"

    conn.close()
    return redirect('/')


# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect('/')


# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


app.run(debug=True)
