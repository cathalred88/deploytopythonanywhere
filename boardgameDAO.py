## bookDAO.py
## SQLite Version

import sqlite3

class boardgameDAO:

    def __init__(self):
        # Path to SQLite database file
        self.db = "boardgames.sqlite"

    # -------------------------
    # Database Connection
    # -------------------------
    def getConnection(self):
        connection = sqlite3.connect(self.db)
        connection.row_factory = sqlite3.Row  # Allows dict-style access
        return connection

    # -------------------------
    # Convert Row to Dict
    # -------------------------
    def convertToDictionary(self, row):
        return {
            "id": row["id"],
            "bgg_id": row["bgg_id"],
            "name": row["name"],
            "year_published": row["year_published"],
            "min_players": row["min_players"],
            "max_players": row["max_players"],
            "playtime": row["playtime"],
            "category": row["category"]
        }

    # -------------------------
    # Get All Board Games
    # -------------------------
    def getAll(self):
        connection = self.getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM boardgames")
        results = cursor.fetchall()

        boardgames = [self.convertToDictionary(row) for row in results]

        connection.close()
        return boardgames

    # -------------------------
    # Find By ID
    # -------------------------
    def findByID(self, id):
        connection = self.getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM boardgames WHERE id = ?", (id,))
        result = cursor.fetchone()

        connection.close()

        if result:
            return self.convertToDictionary(result)
        return None

    # -------------------------
    # Create Board Game
    # -------------------------
    def create(self, boardgame):
        connection = self.getConnection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO boardgames (bgg_id, name, year_published, min_players, max_players, playtime, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (boardgame["bgg_id"], boardgame["name"], boardgame["year_published"], boardgame["min_players"], boardgame["max_players"], boardgame["playtime"], boardgame["category"])
        )

        connection.commit()
        boardgame["id"] = cursor.lastrowid

        connection.close()
        return boardgame

    # -------------------------
    # Update Board Game
    # -------------------------
    def update(self, id, boardgame):
        connection = self.getConnection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE boardgames SET bgg_id = ?, name = ?, year_published = ?, min_players = ?, max_players = ?, playtime = ?, category = ? WHERE id = ?",
            (boardgame["bgg_id"], boardgame["name"], boardgame["year_published"], boardgame["min_players"], boardgame["max_players"], boardgame["playtime"], boardgame["category"], id)
        )

        connection.commit()
        connection.close()

        boardgame["id"] = id
        return boardgame

    # -------------------------
    # Delete Board Game
    # -------------------------
    def delete(self, id):
        connection = self.getConnection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM boardgames WHERE id = ?", (id,))
        connection.commit()
        connection.close()

        return {"message": "Board game deleted"}

    #-------------------------
    # filter by number of players 
    #-------------------------
    def getAll(self, min_players=None, max_playtime=None):
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = "SELECT * FROM boardgames WHERE 1=1"
        params = []

        # Filter by minimum player count
        if min_players is not None:
            query += " AND min_players <= ? AND max_players >= ?"
            params.append(min_players)
            params.append(min_players)

        # Filter by maximum playtime
        if max_playtime is not None:
            query += " AND playtime <= ?"
            params.append(max_playtime)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]