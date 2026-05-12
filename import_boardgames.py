## import_boardgames.py
## Author Cathal Redmond
## Date 12 May 2026
## This script imports board game data from a xml file on a website calledboardgamegeek.com into the SQLite database.`
import requests
import sqlite3
import xml.etree.ElementTree as ET
import time

DB = "boardgames.sqlite"

def fetch_hot_games():
    url = "https://boardgamegeek.com/xmlapi2/hot?type=boardgame"

    headers = {
        "User-Agent": "BoardGameApp/1.0"
    }

    response = requests.get(url, headers=headers)

    # Handle BGG 202 queued response
    while response.status_code == 202:
        print("BGG processing request... waiting 5 seconds")
        time.sleep(5)
        response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response.text


def parse_and_store(xml_data):

    # ✅ DEFENSIVE CHECK GOES HERE
    if not xml_data.strip().startswith("<"):
        print("Response was not valid XML!")
        print(xml_data[:500])
        return

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