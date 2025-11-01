from flask import Flask, render_template, request, redirect
import sqlite3, os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Create table
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS found_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  description TEXT,
                  image TEXT,
                  location TEXT,
                  date TEXT)''')
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report_lost')
def report_lost():
    return render_template('rp_L.html')

@app.route('/report_found')
def report_found():
    return render_template('rp_F.html')

@app.route('/sign-in')
def signin():
    return render_template('signin.html')

@app.route('/items')
def items():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute("SELECT * FROM found_items ORDER BY id DESC")
    all_items = cursor.fetchall()
    conn.close()
    return render_template('items.html', items=all_items)

@app.route('/add', methods=['POST'])
def add_item():
    title = request.form['item-title-found']
    description = request.form['item-description-found']
    location = request.form['item-location-found']
    date = request.form['item-date-found']

    # handle image upload
    image_file = request.files['item-image-found']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(image_path)

    # save data to db
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO found_items (title, description, image, location, date) VALUES (?, ?, ?, ?, ?)",
                 (title, description, image_file.filename, location, date))
    conn.commit()
    conn.close()

    return redirect('/items')

if __name__=="__main__":
    app.run()