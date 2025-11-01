from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

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

        conn = sqlite3.connect('lostandfound.db')
        c = conn.cursor()

        c.execute("""
            INSERT INTO items (title, description, location, date, type, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            title,
            description,
            location,
            date,
            "Lost",
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

        conn = sqlite3.connect('lostandfound.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO items (title, description, location, date, type, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            title,
            description,
            location,
            date,
            "Found",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('rp_F.html')\

@app.route('/items')
def items():
    conn = sqlite3.connect('lostandfound.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY id DESC")
    items = c.fetchall()
    conn.close()
    return render_template('items.html', items=items)

if __name__=="__main__":
    app.run(debug=True)