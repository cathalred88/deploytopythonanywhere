## server.py
## Author Cathal Redmond
## Web Services & Applications - Big Project
## SQLite Version

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from boardgameDAO import boardgameDAO

app = Flask(__name__)
CORS(app, supports_credentials=True)

dao = boardgameDAO()


# -------------------------------------
# Create Database & Table if Missing
# -------------------------------------
def init_db():
    conn = sqlite3.connect("boardgames.sqlite")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS boardgames (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bgg_id INTEGER,
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


init_db()


# -------------------------------------
# Serve Frontend
# -------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------------------------
# API ROUTES
# -------------------------------------

# GET all board games
@app.route("/boardgames", methods=["GET"])
def getAll():
    return jsonify(dao.getAll())


# GET board game by ID
@app.route("/boardgames/<int:id>", methods=["GET"])
def findById(id):
    boardgame = dao.findByID(id)
    if boardgame is None:
        return jsonify({"error": "Board game not found"}), 404
    return jsonify(boardgame)


# CREATE board game
@app.route("/boardgames", methods=["POST"])
def create():
    boardgame = request.json

    if not boardgame:
        return jsonify({"error": "Invalid input"}), 400

    if "name" not in boardgame:
        return jsonify({"error": "Missing required fields"}), 400

    return jsonify(dao.create(boardgame)), 201


# UPDATE board game
@app.route("/boardgames/<int:id>", methods=["PUT"])
def update(id):
    boardgame = request.json

    if not boardgame:
        return jsonify({"error": "Invalid input"}), 400

    existing = dao.findByID(id)
    if existing is None:
        return jsonify({"error": "Board game not found"}), 404

    return jsonify(dao.update(id, boardgame))


# DELETE board game
@app.route("/boardgames/<int:id>", methods=["DELETE"])
def delete(id):
    existing = dao.findByID(id)
    if existing is None:
        return jsonify({"error": "Board game not found"}), 404

    return jsonify(dao.delete(id))


# FILTER board games by min_players and max_playtime
@app.route('/boardgames', methods=['GET'])
def get_all_games():

    # Get query parameters from URL
    min_players = request.args.get('min_players', type=int)
    max_playtime = request.args.get('max_playtime', type=int)

    games = dao.getAll(min_players=min_players, max_playtime=max_playtime)
    return jsonify(games)

# -------------------------------------
# Run Locally
# -------------------------------------
if __name__ == "__main__":
    app.run(debug=True)