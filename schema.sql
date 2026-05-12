DROP TABLE IF EXISTS boardgames;
CREATE TABLE boardgames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bgg_id INTEGER UNIQUE,
    name TEXT NOT NULL,
    year_published INTEGER,
    min_players INTEGER,
    max_players INTEGER,
    playtime INTEGER
);