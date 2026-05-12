# Title: Web Services & Applications - Big Project

## Author: Cathal Redmond
## Board Game Database Web App

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


## Database

The project uses a SQLite database called:

boardgames.sqlite

The main table is:

CREATE TABLE boardgames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bgg_id INTEGER UNIQUE,
    name TEXT NOT NULL,
    year_published INTEGER,
    min_players INTEGER,
    max_players INTEGER,
    playtime INTEGER,
    category TEXT
);

## API Endpoints
Method	Endpoint	Description
GET	/boardgames	Get all board games
GET	/boardgames/<id>	Get a board game by ID
POST	/boardgames	Create a new board game
PUT	/boardgames/<id>	Update an existing board game
DELETE	/boardgames/<id>	Delete a board game
Filtering

The API supports filtering by player count and maximum playtime.

Example:

/boardgames?min_players=4&max_playtime=30

This returns games that support 4 players and have a playtime of 30 minutes or less.


## Running Locally
1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate
2. Install requirements
pip install -r requirements.txt
3. Create the database schema
python createschema.py
4. Import sample board game data
python import_boardgames.py
5. Run the Flask server
python server.py

Then open: http://127.0.0.1:5000

## Running on PythonAnywhere 
This project is running live on https://cathalred88.pythonanywhere.com/ to view and interact with. 
