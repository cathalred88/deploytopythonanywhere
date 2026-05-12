## boardgameDAO.py
## SQLite Version


import sqlite3

class boardgameDAO:

    def __init__(self):
        self.db = "boardgames.sqlite"

    def dict_factory(self, cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    def getAll(self, min_players=None, max_playtime=None):
        conn = sqlite3.connect(self.db)
        conn.row_factory = self.dict_factory
        cursor = conn.cursor()

        query = "SELECT * FROM boardgames WHERE 1=1"
        params = []

        if min_players is not None:
            query += " AND min_players <= ? AND max_players >= ?"
            params.append(min_players)
            params.append(min_players)

        if max_playtime is not None:
            query += " AND playtime <= ?"
            params.append(max_playtime)

        cursor.execute(query, params)
        games = cursor.fetchall()

        conn.close()
        return games

    def findByID(self, id):
        conn = sqlite3.connect(self.db)
        conn.row_factory = self.dict_factory
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM boardgames WHERE id = ?", (id,))
        game = cursor.fetchone()

        conn.close()
        return game

    def create(self, game):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO boardgames
            (name, year_published, min_players, max_players, playtime, category)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            game.get("name"),
            game.get("year_published"),
            game.get("min_players"),
            game.get("max_players"),
            game.get("playtime"),
            game.get("category", "")
        ))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return self.findByID(new_id)

    def update(self, id, game):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE boardgames
            SET name = ?,
                year_published = ?,
                min_players = ?,
                max_players = ?,
                playtime = ?,
                category = ?
            WHERE id = ?
        """, (
            game.get("name"),
            game.get("year_published"),
            game.get("min_players"),
            game.get("max_players"),
            game.get("playtime"),
            game.get("category", ""),
            id
        ))

        conn.commit()
        conn.close()

        return self.findByID(id)

    def delete(self, id):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM boardgames WHERE id = ?", (id,))
        conn.commit()
        conn.close()

        return {"message": "Board game deleted successfully"}