import sqlite3

conn = sqlite3.connect('lostandfound.db')
c = conn.cursor()

# ⚠️ This will delete ALL rows in the items table
c.execute("DELETE FROM items")

conn.commit()
conn.close()

