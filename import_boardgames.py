# import_boardgames.py
# Author: Cathal Redmond
# Description: Import sample board games and optionally import a small batch
# from recommend.games JSON endpoints.

import time
import sqlite3
import requests

DB = "boardgames.sqlite"
API_BASE = "https://recommend.games/api/"
DELAY_SECONDS = 1
BATCH_SIZE = 10


SAMPLE_BOARDGAMES = [
    (13, "Catan", 1995, 3, 4, 90, "Strategy"),
    (822, "Carcassonne", 2000, 2, 5, 45, "Tile Placement"),
    (68448, "7 Wonders", 2010, 2, 7, 30, "Card Drafting"),
    (178900, "Codenames", 2015, 2, 8, 15, "Party"),
    (167791, "Terraforming Mars", 2016, 1, 5, 120, "Strategy"),
    (30549, "Pandemic", 2008, 2, 4, 45, "Cooperative"),
    (266192, "Wingspan", 2019, 1, 5, 70, "Engine Building"),
    (230802, "Azul", 2017, 2, 4, 45, "Abstract"),
    (36218, "Dominion", 2008, 2, 4, 30, "Deck Building"),
    (9209, "Ticket to Ride", 2004, 2, 5, 60, "Family"),
    (148228, "Splendor", 2014, 2, 4, 30, "Set Collection"),
    (173346, "7 Wonders Duel", 2015, 2, 2, 30, "Card Drafting"),
    (129622, "Love Letter", 2012, 2, 6, 20, "Deduction"),
    (39856, "Dixit", 2008, 3, 8, 30, "Party"),
    (199792, "Everdell", 2018, 1, 4, 80, "Worker Placement")
]


def get_connection():
    return sqlite3.connect(DB)


def import_sample_boardgames():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT OR IGNORE INTO boardgames
        (bgg_id, name, year_published, min_players, max_players, playtime, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, SAMPLE_BOARDGAMES)

    conn.commit()
    count = cursor.rowcount
    conn.close()

    return count


def fetch_json(url):
    headers = {
        "User-Agent": "CathalBoardGameCourseworkApp/1.0"
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()


def extract_game_ids(data):
    ids = []

    results = data.get("results", [])

    for item in results:
        game_id = item.get("bgg_id")

        if game_id:
            ids.append(game_id)

    print(f"Extracted {len(ids)} game IDs")

    return ids


def parse_game(game_id, data):
    name = (
        data.get("name")
        or data.get("title")
        or data.get("primary_name")
        or f"Imported Game {game_id}"
    )

    year = (
        data.get("year")
        or data.get("year_published")
        or data.get("yearpublished")
    )

    min_players = (
        data.get("min_players")
        or data.get("minplayers")
        or data.get("minPlayerCount")
    )

    max_players = (
        data.get("max_players")
        or data.get("maxplayers")
        or data.get("maxPlayerCount")
    )

    playtime = (
        data.get("playtime")
        or data.get("playingtime")
        or data.get("max_playtime")
        or data.get("maxPlayTime")
    )

    category = (
        data.get("category")
        or data.get("mechanic")
        or data.get("type")
        or "Imported"
    )

    return {
        "bgg_id": game_id,
        "name": name,
        "year_published": year,
        "min_players": min_players,
        "max_players": max_players,
        "playtime": playtime,
        "category": category
    }


def save_game(game):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO boardgames
        (bgg_id, name, year_published, min_players, max_players, playtime, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        game["bgg_id"],
        game["name"],
        game["year_published"],
        game["min_players"],
        game["max_players"],
        game["playtime"],
        game["category"]
    ))

    conn.commit()
    inserted = cursor.rowcount
    conn.close()

    return inserted


def count_imported_external_games():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM boardgames
        WHERE category IS NOT NULL
    """)

    count = cursor.fetchone()[0]

    conn.close()
    return count


def import_from_recommend_games(batch_size=BATCH_SIZE):
    page_size = batch_size

    existing_count = count_imported_external_games()

    page = (existing_count // page_size) + 1

    print(f"Fetching recommend.games page {page}")

    url = API_BASE + f"games.json?page={page}"

    data = fetch_json(url)

    results = data.get("results", [])

    imported_count = 0

    for item in results[:batch_size]:
        try:
            game = {
                "bgg_id": item.get("bgg_id"),
                "name": item.get("name"),
                "year_published": item.get("year"),
                "min_players": item.get("min_players"),
                "max_players": item.get("max_players"),
                "playtime": item.get("playtime"),
                "category": (
                    item.get("game_type_name", ["Imported"])[0]
                    if item.get("game_type_name")
                    else "Imported"
                )
            }

            imported_count += save_game(game)

            print(f"Processed: {game['name']}")

            time.sleep(DELAY_SECONDS)

        except Exception as e:
            print(f"Error importing game: {e}")

    return imported_count


def import_boardgames(batch_size=BATCH_SIZE):
    sample_count = import_sample_boardgames()

    try:
        external_count = import_from_recommend_games(batch_size=batch_size)
    except Exception as e:
        print(f"External import failed: {e}")
        external_count = 0

    return sample_count + external_count


if __name__ == "__main__":
    count = import_boardgames()
    print(f"{count} board games imported.")