// app.js
// Author: Cathal Redmond using Chat GPT Prompt: "Please create for me a client-side application that will interact with an API that performs CRUD operations on books. Use jQuery AJAX for the API calls. Put the HTML, CSS, and Javascript in separate files"
// Date: 2026-May-07


const API_URL = "/boardgames";

async function loadGames() {

    const players = document.getElementById("playersInput").value;
    const playtime = document.getElementById("playtimeInput").value;

    let url = API_URL;

    const params = new URLSearchParams();

    if (players) {
        params.append("min_players", players);
    }

    if (playtime) {
        params.append("max_playtime", playtime);
    }

    if (params.toString()) {
        url += "?" + params.toString();
    }

    try {
        const response = await fetch(url);
        const games = await response.json();

        displayGames(games);

    } catch (error) {
        console.error("Error loading games:", error);
    }
}

function displayGames(games) {

    const tbody = document.getElementById("gamesBody");
    tbody.innerHTML = "";

    if (games.length === 0) {
        tbody.innerHTML = "<tr><td colspan='4'>No games found</td></tr>";
        return;
    }

    games.forEach(game => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${game.name}</td>
            <td>${game.year_published || "N/A"}</td>
            <td>${game.min_players} - ${game.max_players}</td>
            <td>${game.playtime} mins</td>
        `;

        tbody.appendChild(row);
    });
}

function clearFilters() {
    document.getElementById("playersInput").value = "";
    document.getElementById("playtimeInput").value = "";
    loadGames();
}

// Load all games on page load
window.onload = loadGames;