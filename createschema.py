import sqlite3

conn = sqlite3.connect("boardgames.sqlite")
cursor = conn.cursor()

# Delete old table during development
cursor.execute("DROP TABLE IF EXISTS boardgames")

# Create updated table
cursor.execute("""
CREATE TABLE boardgames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bgg_id INTEGER UNIQUE,
    name TEXT NOT NULL,
    year_published INTEGER,
    min_players INTEGER,
    max_players INTEGER,
    playtime INTEGER,
    category TEXT
)
""")

conn.commit()
conn.close()

print("Boardgames database schema created successfully.")