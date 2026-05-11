import sqlite3

conn = sqlite3.connect("bookdb.sqlite")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    price REAL NOT NULL
)
""")

conn.commit()
conn.close()

print("Database schema created successfully.")