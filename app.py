from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
from datetime import datetime
import os
from functools import wraps #ตัวตรวจสอบสิทธิ์ Admin

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here'


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # ตรวจสอบว่ามี session หรือไม่ และ role เป็น 'admin' หรือไม่
        if session.get('role') != 'admin':
            flash("You must be an admin to view this page.", "error")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    conn = sqlite3.connect('lostandfound.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE type='Lost' ORDER BY id DESC")
    lost_items = [dict(row) for row in c.fetchall()] 
    c.execute("SELECT * FROM items WHERE type='Found' ORDER BY id DESC")
    found_items = [dict(row) for row in c.fetchall()]
    conn.close()
    return render_template('index.html', 
                           lost_items=lost_items, 
                           found_items=found_items,
                           lost_items_json=jsonify(lost_items).get_data(as_text=True),
                           found_items_json=jsonify(found_items).get_data(as_text=True))


@app.route('/report_lost', methods=['GET', 'POST'])
def report_lost():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        location = request.form['location']

        imageName = None 
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                imageName = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_FOLDER, imageName))

        conn = sqlite3.connect('lostandfound.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO items (title, description, date, type, created_at, image, latitude, longitude, location)
            VALUES (?, ?, ?, 'Lost', ?, ?, ?, ?, ?)
        """, (title, description, date, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), imageName, latitude, longitude, location))
        
        conn.commit()
        conn.close()
        flash("Lost item reported successfully!", "success")
        return redirect(url_for('index'))

    return render_template('rp_L.html')

@app.route('/report_found', methods=['GET', 'POST'])
def report_found():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        location = request.form['location']

        imageName = None 
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                imageName = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_FOLDER, imageName))

        conn = sqlite3.connect('lostandfound.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO items (title, description, date, type, created_at, image, latitude, longitude, location)
            VALUES (?, ?, ?, 'Found', ?, ?, ?, ?, ?)
        """, (title, description, date, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), imageName, latitude, longitude, location))
        
        conn.commit()
        conn.close()
        flash("Found item reported successfully!", "success")
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

@app.route('/admin/manage')
@admin_required  # <-- ใช้ตัวตรวจสอบสิทธิ์ที่เราเพิ่งสร้าง
def admin_manage():
    conn = sqlite3.connect('lostandfound.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY id DESC")
    items = c.fetchall()
    conn.close()
    return render_template('admin_manage.html', items=items)


@app.route('/admin/edit/<int:item_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit(item_id):
    conn = sqlite3.connect('lostandfound.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        item_type = request.form['type']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        location = request.form.get('location', '')

        c.execute("""
            UPDATE items 
            SET title = ?, description = ?, date = ?, type = ?,
                latitude = ?, longitude = ?, location = ?
            WHERE id = ?
        """, (title, description, date, item_type, 
              latitude, longitude, location, 
              item_id))
        
        conn.commit()
        conn.close()
        flash("Item updated successfully!", "success")
        return redirect(url_for('admin_manage'))

    c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = c.fetchone()
    conn.close()
    
    if item is None:
        flash("Item not found!", "error")
        return redirect(url_for('admin_manage'))

    return render_template('admin_edit.html', item=item)


@app.route('/admin/delete/<int:item_id>')
@admin_required
def admin_delete(item_id):
    conn = sqlite3.connect('lostandfound.db')
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    flash("Item deleted successfully!", "success")
    return redirect(url_for('admin_manage'))

if __name__=="__main__":
    app.run(debug=True)