## bookDAO.py
## SQLite Version

import sqlite3

class BookDAO:

    def __init__(self):
        # Path to SQLite database file
        self.database = "books.db"

    # -------------------------
    # Database Connection
    # -------------------------
    def getConnection(self):
        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row  # Allows dict-style access
        return connection

    # -------------------------
    # Convert Row to Dict
    # -------------------------
    def convertToDictionary(self, row):
        return {
            "id": row["id"],
            "title": row["title"],
            "author": row["author"],
            "price": float(row["price"])
        }

    # -------------------------
    # Get All Books
    # -------------------------
    def getAll(self):
        connection = self.getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books")
        results = cursor.fetchall()

        books = [self.convertToDictionary(row) for row in results]

        connection.close()
        return books

    # -------------------------
    # Find By ID
    # -------------------------
    def findByID(self, id):
        connection = self.getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
        result = cursor.fetchone()

        connection.close()

        if result:
            return self.convertToDictionary(result)
        return None

    # -------------------------
    # Create Book
    # -------------------------
    def create(self, book):
        connection = self.getConnection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
            (book["title"], book["author"], book["price"])
        )

        connection.commit()
        book["id"] = cursor.lastrowid

        connection.close()
        return book

    # -------------------------
    # Update Book
    # -------------------------
    def update(self, id, book):
        connection = self.getConnection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE books SET title = ?, author = ?, price = ? WHERE id = ?",
            (book["title"], book["author"], book["price"], id)
        )

        connection.commit()
        connection.close()

        book["id"] = id
        return book

    # -------------------------
    # Delete Book
    # -------------------------
    def delete(self, id):
        connection = self.getConnection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM books WHERE id = ?", (id,))
        connection.commit()
        connection.close()

        return {"message": "Book deleted"}