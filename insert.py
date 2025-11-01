import sqlite3
from datetime import datetime

conn = sqlite3.connect("lostandfound.db")
c = conn.cursor()

c.execute("""
INSERT INTO items (title, description, location, date, type, created_at)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    "Lost Wallet",
    "Black leather wallet near cafeteria",
    "Campus Cafeteria",
    "2025-11-01",
    "Lost",
    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
))

conn.commit()
conn.close()
