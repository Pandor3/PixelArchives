console.log('Fichier JS Chargé');

fetch("/static/data/games.json")
    .then(response => response.json())
    .then(data => {
        console.log(data);

        /* Ceci permet de trier les jeux du plus ancien au plus récent */
        data.sort((nouveau, ancien) => nouveau.year - ancien.year);

        /* Ceci permet de classer les consoles dans un tableau en lisant les cartes de jeu */
        let uniqueConsoles = [];
        data.forEach(game => {
            game.console.forEach(consoleName => {
                if (!uniqueConsoles.includes(consoleName)) {
                    uniqueConsoles.push(consoleName);
                }
            });
        });

        /* Ceci permet de filtrer les...Filtres des consoles générés dynamiquement */
        uniqueConsoles.sort()

        /* Ceci permet de classer les genres dans un tableau en lisant les cartes de jeu */
        let uniqueGenres = [];
        data.forEach(game => {
            game.genre.forEach(genreName => {
                if (!uniqueGenres.includes(genreName)) {
                    uniqueGenres.push(genreName);
                }
            });
        });

        /* Ceci permet de filtrer les filtres des genres générés dynamiquement */
        uniqueGenres.sort();

        /* Ceci permet de mettre les consoles dans le système de filtrage */
        const selectElement = document.getElementById('consoles-select');
        uniqueConsoles.forEach(consoleName => {
            const option = document.createElement('option');
            option.textContent = consoleName;
            option.value = consoleName;
            selectElement.appendChild(option);
        });

        /* Ceci permet de mettre les genres dans le système de filtrage */
        const selectGenre = document.getElementById('genres-select');
        uniqueGenres.forEach(genreName => {
            const option = document.createElement('option');
            option.textContent = genreName;
            option.value = genreName;
            selectGenre.appendChild(option);
        });
        
        const gallery = document.getElementById('game-gallery');
        
        /* Ceci permet la création des cartes de jeux dynamiquement */
        function showGames(list) {
            list.forEach(game => {
                const card = document.createElement('div');
                card.classList.add('game-card');

                const img = document.createElement("img");
                img.src = game.cover || "./assets/img/placeholder.jpg";
                img.alt = `Jaquette de ${game.title}`;
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

                gallery.appendChild(card);
        });
    }

    /* Ceci est une fonction permettant de filtrer les jeux et les genres */
    function filterGames() {
            const selectedConsole = selectElement.value;
            const selectedGenre = selectGenre.value;

            const filteredGames = data.filter(game => {
                const matchConsole = (selectedConsole === "all") || game.console.includes(selectedConsole);
                const matchGenre = (selectedGenre === "all") || game.genre.includes(selectedGenre);
                return matchConsole && matchGenre;
            });

            gallery.innerHTML = "";
            showGames(filteredGames);
        }
    
        /* Ceci sont deux listeners qui permettent de changer la page en fonction des filtres choisis */
    selectElement.addEventListener('change', filterGames);
    selectGenre.addEventListener('change', filterGames);
    showGames(data);
});
