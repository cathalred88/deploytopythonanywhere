// app.js
// Author: Cathal Redmond using Chat GPT Prompt: "Please create for me a client-side application that will interact with an API that performs CRUD operations on books. Use jQuery AJAX for the API calls. Put the HTML, CSS, and Javascript in separate files"
// Date: 2026-May-07




const API_URL = "/boardgames";

let games = [];
let sortColumn = null;
let sortDirection = "asc";

document.addEventListener("DOMContentLoaded", function () {
    loadGames();
});

async function loadGames() {
    const players = document.getElementById("playersInput").value;
    const playtime = document.getElementById("playtimeInput").value;

    const params = new URLSearchParams();

    if (players) {
        params.append("min_players", players);
    }

    if (playtime) {
        params.append("max_playtime", playtime);
    }

    let url = API_URL;

    if (params.toString()) {
        url += "?" + params.toString();
    }

    const response = await fetch(url);
    games = await response.json();

    displayGames(games);
}

function displayGames(gameList) {
    const tbody = document.getElementById("gamesBody");
    tbody.innerHTML = "";

    if (!gameList || gameList.length === 0) {
        tbody.innerHTML = "<tr><td colspan='8'>No games found</td></tr>";
        return;
    }

    gameList.forEach(game => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${game.id}</td>
            <td>${game.name}</td>
            <td>${game.year_published ?? ""}</td>
            <td>${game.min_players ?? ""}</td>
            <td>${game.max_players ?? ""}</td>
            <td>${game.playtime ?? ""}</td>
            <td>${game.category ?? ""}</td>
            <td>
                <button type="button" onclick="editGame(${game.id})">Edit</button>
                <button type="button" class="danger" onclick="deleteGame(${game.id})">Delete</button>
            </td>
        `;

        tbody.appendChild(row);
    });
}

async function saveGame() {
    const id = document.getElementById("gameId").value;

    const game = {
        name: document.getElementById("name").value,
        year_published: parseInt(document.getElementById("year_published").value),
        min_players: parseInt(document.getElementById("min_players").value),
        max_players: parseInt(document.getElementById("max_players").value),
        playtime: parseInt(document.getElementById("playtime").value),
        category: document.getElementById("category").value
    };

    if (!game.name) {
        alert("Please enter a game name.");
        return;
    }

    const url = id ? `${API_URL}/${id}` : API_URL;
    const method = id ? "PUT" : "POST";

    const response = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(game)
    });

    if (!response.ok) {
        alert("Save failed.");
        console.error(await response.text());
        return;
    }

    clearForm();
    loadGames();
}

function editGame(id) {
    const game = games.find(g => g.id === id);

    if (!game) {
        alert("Game not found.");
        return;
    }

    document.getElementById("gameId").value = game.id;
    document.getElementById("name").value = game.name;
    document.getElementById("year_published").value = game.year_published ?? "";
    document.getElementById("min_players").value = game.min_players ?? "";
    document.getElementById("max_players").value = game.max_players ?? "";
    document.getElementById("playtime").value = game.playtime ?? "";
    document.getElementById("category").value = game.category ?? "";

    document.getElementById("formTitle").textContent = "Update Board Game";
}

async function deleteGame(id) {
    if (!confirm("Delete this board game?")) {
        return;
    }

    const response = await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });

    if (!response.ok) {
        alert("Delete failed.");
        return;
    }

    loadGames();
}

function clearForm() {
    document.getElementById("gameId").value = "";
    document.getElementById("name").value = "";
    document.getElementById("year_published").value = "";
    document.getElementById("min_players").value = "";
    document.getElementById("max_players").value = "";
    document.getElementById("playtime").value = "";
    document.getElementById("category").value = "";

    document.getElementById("formTitle").textContent = "Add New Board Game";
}

function clearFilters() {
    document.getElementById("playersInput").value = "";
    document.getElementById("playtimeInput").value = "";
    loadGames();
}

function sortTable(column) {
    if (sortColumn === column) {
        sortDirection = sortDirection === "asc" ? "desc" : "asc";
    } else {
        sortColumn = column;
        sortDirection = "asc";
    }

    const sortedGames = [...games].sort((a, b) => {
        let valueA = a[column];
        let valueB = b[column];

        if (valueA === null || valueA === undefined) valueA = "";
        if (valueB === null || valueB === undefined) valueB = "";

        if (typeof valueA === "string") {
            valueA = valueA.toLowerCase();
            valueB = valueB.toLowerCase();
        }

        if (valueA < valueB) {
            return sortDirection === "asc" ? -1 : 1;
        }

        if (valueA > valueB) {
            return sortDirection === "asc" ? 1 : -1;
        }

        return 0;
    });

    displayGames(sortedGames);
}