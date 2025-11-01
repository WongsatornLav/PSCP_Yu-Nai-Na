import sqlite3

conn = sqlite3.connect("lostandfound.db")
c =  conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    location TEXT,
    date TEXT,
    type TEXT,
    created_at TEXT
);
""")

conn.commit()
conn.close()
