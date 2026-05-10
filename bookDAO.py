## bookDAO.py
## Author Cathal Redmond
## Data 05 May 2026

# This file will be used to develop the code for the big project for Web services and Applications coursework. 
# It will be used to test the functionality of the code as it is developed.
# renamed from test.py to bookDAO.py on 06 May 2026to better reflect its purpose as a data access object for the books in the REST API.

# imports
import mysql.connector

class BookDAO:

    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "bookdb"

    # -------------------------
    # Database Connection
    # -------------------------
    def getConnection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    # -------------------------
    # Convert DB row to Dict
    # -------------------------
    def convertToDictionary(self, resultLine):
        return {
            "id": resultLine[0],
            "title": resultLine[1],
            "author": resultLine[2],
            "price": float(resultLine[3])
        }

    # -------------------------
    # Get All Books
    # -------------------------
    def getAll(self):
        connection = self.getConnection()
        cursor = connection.cursor()
        sql = "SELECT * FROM books"
        cursor.execute(sql)
        results = cursor.fetchall()

        books = []
        for row in results:
            books.append(self.convertToDictionary(row))

        cursor.close()
        connection.close()
        return books

    # -------------------------
    # Find By ID
    # -------------------------
    def findByID(self, id):
        connection = self.getConnection()
        cursor = connection.cursor()
        sql = "SELECT * FROM books WHERE id = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()

        cursor.close()
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
        sql = "INSERT INTO books (title, author, price) VALUES (%s, %s, %s)"
        values = (book["title"], book["author"], book["price"])
        cursor.execute(sql, values)
        connection.commit()

        book["id"] = cursor.lastrowid

        cursor.close()
        connection.close()
        return book

    # -------------------------
    # Update Book
    # -------------------------
    def update(self, id, book):
        connection = self.getConnection()
        cursor = connection.cursor()
        sql = "UPDATE books SET title=%s, author=%s, price=%s WHERE id=%s"
        values = (book["title"], book["author"], book["price"], id)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        book["id"] = id
        return book

    # -------------------------
    # Delete Book
    # -------------------------
    def delete(self, id):
        connection = self.getConnection()
        cursor = connection.cursor()
        sql = "DELETE FROM books WHERE id = %s"
        values = (id,)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return {"message": "Book deleted"}