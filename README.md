# Board Game Database Web App

## Overview

This project is a Flask-based web application for managing a board game database.  
It allows users to view, create, update, delete, filter, and sort board games through a browser-based interface.

The project was originally built as a book database and was later adapted into a board game database.

---

## Features

- View all board games
- Add new board games
- Update existing board games
- Delete board games
- Filter games by player count
- Filter games by maximum playtime
- Sort table columns
- SQLite database storage
- Flask REST API backend
- HTML, CSS, and JavaScript frontend
- Deployed using PythonAnywhere

---

## Technologies Used

- Python
- Flask
- Flask-CORS
- SQLite
- HTML
- CSS
- JavaScript
- PythonAnywhere

---

## Project Structure


deploytopythionanywhere/
│
├── server.py
├── boardgameDAO.py
├── createschema.py
├── import_boardgames.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── styles.css
    │
    └── js/
        └── app.js