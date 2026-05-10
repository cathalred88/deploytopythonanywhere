## restServer.py
## Author Cathal Redmond
## Data 05 May 2026
# This is the main REST server file for the big project for Web services and Applications coursework.

# imports
from flask import Flask, request, jsonify, abort, render_template
from flask_cors import CORS
from bookDAO import BookDAO

# Create Flask app
app = Flask(__name__)
CORS(app)

# Create DAO instance
book_dao = BookDAO()


# -------------------------
# Welcome Route
# -------------------------
@app.route('/')
def index():
    return render_template('index.html')


# -------------------------
# GET All Books
# -------------------------
@app.route('/books', methods=['GET'])
def getAll():
    return jsonify(book_dao.getAll())


# -------------------------
# GET Book By ID
# -------------------------
@app.route('/books/<int:id>', methods=['GET'])
def findByID(id):
    book = book_dao.findByID(id)
    if book is None:
        abort(404, description="Book not found")
    return jsonify(book)


# -------------------------
# CREATE Book
# -------------------------
@app.route('/books', methods=['POST'])
def create():
    if not request.json:
        abort(400, description="Request must be JSON")

    required_fields = ["title", "author", "price"]

    for field in required_fields:
        if field not in request.json:
            abort(400, description=f"{field} is required")

    book = {
        "title": request.json["title"],
        "author": request.json["author"],
        "price": request.json["price"]
    }

    created_book = book_dao.create(book)
    return jsonify(created_book), 201


# -------------------------
# UPDATE Book
# -------------------------
@app.route('/books/<int:id>', methods=['PUT'])
def update(id):
    book = book_dao.findByID(id)
    if book is None:
        abort(404, description="Book not found")

    if not request.json:
        abort(400, description="Request must be JSON")

    updatedBook = {
        "title": request.json.get("title", book["title"]),
        "author": request.json.get("author", book["author"]),
        "price": request.json.get("price", book["price"])
    }

    result = book_dao.update(id, updatedBook)
    return jsonify(result)


# -------------------------
# DELETE Book
# -------------------------
@app.route('/books/<int:id>', methods=['DELETE'])
def delete(id):
    result = book_dao.delete(id)
    if result is None:
        abort(404, description="Book not found")
    return jsonify({"message": "Book deleted"})


# -------------------------
# Run Server
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)