import sqlite3

conn = sqlite3.connect("lostandfound.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    location TEXT,
    date TEXT,
    type TEXT,
    image TEXT,
    created_at TEXT,
    latitude REAL,
    longitude REAL,
    contact TEXT
);
""")

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);
''')

c.execute('''UPDATE users SET role = 'admin' WHERE id = 1;''')

conn.commit()
conn.close()
