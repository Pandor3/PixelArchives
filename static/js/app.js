console.log('Fichier JS Chargé');

const userUuid = localStorage.getItem('uuid');
let userCollectionIds = [];

// Récupération des IDs des jeux ajoutés par l'utilisateur
function getUserCollection() {
    return fetch("/api/profil", { credentials: 'include' })
        .then(res => {
            if (!res.ok) throw new Error("Utilisateur non connecté");
            return res.json();
        })
        .then(data => {
            if (Array.isArray(data.collection)) {
                userCollectionIds = data.collection.map(game => game.id);
            }
        })
        .catch(() => {
            userCollectionIds = [];
        });
}


// Ceci va charger tous les jeux depuis la base
fetch("/api/games")
    .then(response => response.json())
    .then(data => {
        console.log(data);

        // Trie les jeux du plus ancien au plus récent
        data.sort((a, b) => a.year - b.year);

        let uniqueConsoles = [];
        let uniqueGenres = [];

        // Normalise les champs console/genre (string → tableau)
        data.forEach(game => {
            if (typeof game.console === "string") {
                game.console = game.console.split(',').map(s => s.trim());
            }
            if (typeof game.genre === "string") {
                game.genre = game.genre.split(',').map(s => s.trim());
            }

            game.console.forEach(consoleName => {
                if (!uniqueConsoles.includes(consoleName)) {
                    uniqueConsoles.push(consoleName);
                }
            });

            game.genre.forEach(genreName => {
                if (!uniqueGenres.includes(genreName)) {
                    uniqueGenres.push(genreName);
                }
            });
        });

        // Trie alphabétique
        uniqueConsoles.sort();
        uniqueGenres.sort();

        const selectElement = document.getElementById('consoles-select');
        uniqueConsoles.forEach(consoleName => {
            const option = document.createElement('option');
            option.textContent = consoleName;
            option.value = consoleName;
            selectElement.appendChild(option);
        });

        const selectGenre = document.getElementById('genres-select');
        uniqueGenres.forEach(genreName => {
            const option = document.createElement('option');
            option.textContent = genreName;
            option.value = genreName;
            selectGenre.appendChild(option);
        });

        const gallery = document.getElementById('game-gallery');

        // Affiche les cartes de jeux
        function showGames(list) {
            gallery.innerHTML = "";

            list.forEach(game => {
                const card = document.createElement('div');
                card.classList.add('game-card');

                const img = document.createElement("img");
                img.src = `/static/img/${game.cover}`;
                img.alt = `Jaquette de ${game.title}`;
                img.onerror = () => {
                    img.src = "/static/img/placeholder.png";
                };
                card.appendChild(img);

                const title = document.createElement('h2');
                title.textContent = game.title;
                card.appendChild(title);

                const year = document.createElement('p');
                year.textContent = "Année : " + game.year;
                card.appendChild(year);

                const consoles = document.createElement('p');
                consoles.textContent = "Consoles : " + game.console.join(", ");
                card.appendChild(consoles);

                const genres = document.createElement('p');
                genres.textContent = "Genres : " + game.genre.join(", ");
                card.appendChild(genres);

                // Bouton d'ajout à la collection
                const addButton = document.createElement('button');
                addButton.classList.add('collection-btn');
                addButton.textContent = "Ajouter à la collection";
                addButton.dataset.id = game.id;

                // Si le jeu est déjà dans la collection, grise le bouton
                if (userCollectionIds.includes(game.id)) {
                    addButton.disabled = true;
                    addButton.textContent = "Déjà ajouté !";
                    addButton.style.opacity = "0.5";
                    addButton.style.cursor = "not-allowed";
                } else {
                    // Sinon, ajoute le jeu à la collection
                    addButton.addEventListener('click', () => {
                        fetch('/api/users/add_game', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            credentials: 'include',
                            body: JSON.stringify({ game_id: game.id })
                        })
                        .then(res => {
                            if (!res.ok) {
                                if (res.status === 401) {
                                    alert("Vous devez être connecté pour ajouter un jeu !");
                                } else {
                                    throw new Error("Erreur lors de l'ajout !");
                                }
                            } else {
                                return res.json();
                            }
                        })
                        .then(data => {
                            if (data) {
                                alert(data.message || "Jeu ajouté !");
                                // Grise le bouton
                                addButton.disabled = true;
                                addButton.textContent = "Déjà ajouté";
                                addButton.style.opacity = "0.5";
                                addButton.style.cursor = "not-allowed";
                                userCollectionIds.push(game.id); // Ajoute à la liste côté client
                            }
                        })
                        .catch(err => {
                            console.error(err);
                            alert("Erreur : Ajout impossible.");
                        });
                    });
                }

                card.appendChild(addButton);
                gallery.appendChild(card);
            });
        }

        // Fonction de filtrage
        function filterGames() {
            const selectedConsole = selectElement.value;
            const selectedGenre = selectGenre.value;

            const filteredGames = data.filter(game => {
                const matchConsole = (selectedConsole === "all") || game.console.includes(selectedConsole);
                const matchGenre = (selectedGenre === "all") || game.genre.includes(selectedGenre);
                return matchConsole && matchGenre;
            });

            showGames(filteredGames);
        }

        // Listeners
        selectElement.addEventListener('change', filterGames);
        selectGenre.addEventListener('change', filterGames);

        // Lance le tout après avoir récupéré la collection
        getUserCollection().then(() => {
            showGames(data);
        });
    });
