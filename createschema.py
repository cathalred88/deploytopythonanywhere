import sqlite3

# Connect to boardgames database
conn = sqlite3.connect("boardgames.sqlite")
cursor = conn.cursor()

# Drop table if it exists 
cursor.execute("DROP TABLE IF EXISTS boardgames")

# Create boardgames table
cursor.execute("""
CREATE TABLE boardgames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bgg_id INTEGER UNIQUE,
    name TEXT NOT NULL,
    year_published INTEGER,
    min_players INTEGER,
    max_players INTEGER,
    playtime INTEGER
)
""")

conn.commit()
conn.close()

print("Boardgames database schema created successfully.")