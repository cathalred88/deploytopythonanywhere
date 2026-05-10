// app.js
// Author: Cathal Redmond using Chat GPT Prompt: "Please create for me a client-side application that will interact with an API that performs CRUD operations on books. Use jQuery AJAX for the API calls. Put the HTML, CSS, and Javascript in separate files"
// Date: 2026-May-07



const apiUrl = "http://localhost:5000/books";
const AUTH_TOKEN = ""; // Set your auth token here if needed

// Load books on page ready
$(document).ready(function () {
    loadBooks();
});

// =============================
// READ (GET)
// =============================
function loadBooks() {
    $.ajax({
        url: apiUrl,
        type: "GET",
        success: function (books) {
            let rows = "";
            books.forEach(book => {
                rows += `
                    <tr>
                        <td>${book.id}</td>
                        <td>${book.title}</td>
                        <td>${book.author}</td>
                        <td>${book.price}</td>
                        <td>
                            <span class="action-btn" onclick="editBook(${book.id})">Edit</span>
                            <span class="action-btn delete-btn" onclick="deleteBook(${book.id})">Delete</span>
                        </td>
                    </tr>
                `;
            });
            $("#booksTable tbody").html(rows);
        },
        error: function () {
            alert("Error loading books");
        }
    });
}

// =============================
// CREATE & UPDATE
// =============================
$("#bookForm").submit(function (e) {
    e.preventDefault();

    const id = $("#bookId").val();
    const bookData = {
        title: $("#title").val(),
        author: $("#author").val(),
        price: parseFloat($("#price").val())
    };

    if (id) {
        // UPDATE
        $.ajax({
            url: apiUrl + "/" + id,
            type: "PUT",
            contentType: "application/json",
            data: JSON.stringify(bookData),
            success: function () {
                clearForm();
                loadBooks();
            },
            error: function () {
                alert("Error updating book");
            }
        });
    } else {
        // CREATE
        $.ajax({
            url: apiUrl,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(bookData),
            success: function () {
                clearForm();
                loadBooks();
            },
            error: function () {
                alert("Error creating book");
            }
        });
    }
});

// =============================
// EDIT (Populate Form)
// =============================
function editBook(id) {
    $.ajax({
        url: apiUrl + "/" + id,
        type: "GET",
        success: function (book) {
            $("#bookId").val(book.id);
            $("#title").val(book.title);
            $("#author").val(book.author);
            $("#price").val(book.price);
        },
        error: function () {
            alert("Error retrieving book");
        }
    });
}

// =============================
// DELETE
// =============================
function deleteBook(id) {
    if (confirm("Are you sure you want to delete this book?")) {
        $.ajax({
            url: apiUrl + "/" + id,
            type: "DELETE",
            success: function () {
                loadBooks();
            },
            error: function () {
                alert("Error deleting book");
            }
        });
    }
}

// =============================
// CLEAR FORM
// =============================
$("#clearBtn").click(function () {
    clearForm();
});

function clearForm() {
    $("#bookId").val("");
    $("#title").val("");
    $("#author").val("");
    $("#price").val("");
}