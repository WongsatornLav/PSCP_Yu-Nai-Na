from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
from datetime import datetime
import os

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here'


@app.route('/')
def index():
    conn = sqlite3.connect('lostandfound.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE type='Lost' ORDER BY id DESC")
    lost_items = c.fetchall()
    c.execute("SELECT * FROM items WHERE type='Found' ORDER BY id DESC")
    found_items = c.fetchall()
    conn.close()
    return render_template('index.html', lost_items=lost_items, found_items=found_items)


@app.route('/report_lost', methods=['GET', 'POST'])
def report_lost():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        date = request.form['date']
        file = request.files.get('image')
        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        conn = sqlite3.connect('lostandfound.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO items (title, description, location, date, type, image, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            title,
            description,
            location,
            date,
            "Lost",
            filename,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('rp_L.html')

@app.route('/report_found', methods=['GET', 'POST'])
def report_found():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        date = request.form['date']

        file = request.files.get('image')
        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        conn = sqlite3.connect('lostandfound.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO items (title, description, location, date, type, image, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            title,
            description,
            location,
            date,
            "Found",
            filename,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('rp_F.html')

@app.route('/items')
def items():
    conn = sqlite3.connect('lostandfound.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY id DESC")
    items = c.fetchall()
    conn.close()
    return render_template('items.html', items=items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('lostandfound.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            flash(f"Welcome back, {user[1]}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password!", "error")
    return render_template('login.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return render_template('signin.html')

        hashed_pw = generate_password_hash(password)
        role = 'user'
        conn = sqlite3.connect('lostandfound.db')
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed_pw, role)
            )
            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists!", "error")
        finally:
            conn.close()
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
