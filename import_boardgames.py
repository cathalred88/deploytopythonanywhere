## import_boardgames.py
## Author Cathal Redmond
## Date 12 May 2026
## This script imports board game data from a xml file on a website calledboardgamegeek.com into the SQLite database.`

import sqlite3

DB = "boardgames.sqlite"

BOARDGAMES = [
    (13, "Catan", 1995, 3, 4, 90),
    (822, "Carcassonne", 2000, 2, 5, 45),
    (68448, "7 Wonders", 2010, 2, 7, 30),
    (178900, "Codenames", 2015, 2, 8, 15),
    (167791, "Terraforming Mars", 2016, 1, 5, 120),
    (174430, "Gloomhaven", 2017, 1, 4, 120),
    (169786, "Scythe", 2016, 1, 5, 115),
    (30549, "Pandemic", 2008, 2, 4, 45),
    (266192, "Wingspan", 2019, 1, 5, 70),
    (230802, "Azul", 2017, 2, 4, 45),
    (36218, "Dominion", 2008, 2, 4, 30),
    (9209, "Ticket to Ride", 2004, 2, 5, 60),
    (39856, "Dixit", 2008, 3, 8, 30),
    (148228, "Splendor", 2014, 2, 4, 30),
    (31260, "Agricola", 2007, 1, 5, 150),
    (173346, "7 Wonders Duel", 2015, 2, 2, 30),
    (1927, "Munchkin", 2001, 3, 6, 90),
    (129622, "Love Letter", 2012, 2, 6, 20),
    (205637, "Ark Nova", 2021, 1, 4, 150),
    (199792, "Everdell", 2018, 1, 4, 80),
]

def import_boardgames():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT OR IGNORE INTO boardgames
        (bgg_id, name, year_published, min_players, max_players, playtime)
        VALUES (?, ?, ?, ?, ?, ?)
    """, BOARDGAMES)

    conn.commit()
    conn.close()

    print(f"{len(BOARDGAMES)} board games imported successfully.")

if __name__ == "__main__":
    import_boardgames()