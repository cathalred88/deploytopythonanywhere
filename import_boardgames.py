## import_boardgames.py
## Author Cathal Redmond
## Date 12 May 2026
## This script imports board game data from a xml file on a website calledboardgamegeek.com into the SQLite database.`

import requests
import sqlite3
import xml.etree.ElementTree as ET

DB = "boardgames.sqlite"

def fetch_hot_games():
    url = "https://boardgamegeek.com/xmlapi2/hot?type=boardgame"
    response = requests.get(url)
    return response.text

def parse_and_store(xml_data):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    root = ET.fromstring(xml_data)

    for item in root.findall("item"):
        bgg_id = item.attrib["id"]
        name = item.find("name").attrib["value"]
        year = item.find("yearpublished")

        year_val = year.attrib["value"] if year is not None else None

        cursor.execute("""
            INSERT INTO boardgames (bgg_id, name, year_published)
            VALUES (?, ?, ?)
        """, (bgg_id, name, year_val))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    xml_data = fetch_hot_games()
    parse_and_store(xml_data)
    print("Board games imported successfully!")