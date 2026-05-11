## server.py
## Author Cathal Redmond
## Web Services & Applications - Big Project
## SQLite Version

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from bookDAO import BookDAO

app = Flask(__name__)
CORS(app)

dao = BookDAO()


# -------------------------------------
# Create Database & Table if Missing
# -------------------------------------
def init_db():
    conn = sqlite3.connect("bookdb.sqlite")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        price REAL NOT NULL
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

# GET all books
@app.route("/books", methods=["GET"])
def getAll():
    return jsonify(dao.getAll())


# GET book by ID
@app.route("/books/<int:id>", methods=["GET"])
def findById(id):
    book = dao.findByID(id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)


# CREATE book
@app.route("/books", methods=["POST"])
def create():
    book = request.json

    if not book:
        return jsonify({"error": "Invalid input"}), 400

    if "title" not in book or "author" not in book or "price" not in book:
        return jsonify({"error": "Missing required fields"}), 400

    return jsonify(dao.create(book)), 201


# UPDATE book
@app.route("/books/<int:id>", methods=["PUT"])
def update(id):
    book = request.json

    if not book:
        return jsonify({"error": "Invalid input"}), 400

    existing = dao.findByID(id)
    if existing is None:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(dao.update(id, book))


# DELETE book
@app.route("/books/<int:id>", methods=["DELETE"])
def delete(id):
    existing = dao.findByID(id)
    if existing is None:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(dao.delete(id))


# -------------------------------------
# Run Locally
# -------------------------------------
if __name__ == "__main__":
    app.run(debug=True)