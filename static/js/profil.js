document.addEventListener('DOMContentLoaded', () => {
    // Ceci va aller récupérer les informations du profil dans l'API
    fetch('/api/profil')
        .then(response => {
            // Si la réponse est négative = Message d'erreur
            if (!response.ok) {
                throw new Error('Erreur lors de la récupération du profil');
            }
            // Sinon la réponse est convertie en objet JavaScript
            return response.json();
        })
        .then(data => {
            // Ceci permet d'insérer les éléments dans le HTML
            document.getElementById('username').textContent = data.username;
            document.getElementById('email').textContent = data.email;
            // Ceci convertit la date en format plus simple à lire
            document.getElementById('created_at').textContent = new Date(data.created_at).toLocaleDateString();

            const collectionGrid = document.getElementById('user-collection');

            // Ceci va afficher les jaquettes des jeux
            if (data.collection && Array.isArray(data.collection)) {
                collectionGrid.innerHTML = "";

                if (data.collection.length === 0) {
                    collectionGrid.innerHTML = "<p>Aucun jeu dans votre collection pour l'instant...</p>";
                } else {
                    data.collection.forEach(game => {
                        const tile = document.createElement("div");
                        tile.classList.add("game-tile");

                        const img = document.createElement("img");
                        img.src = `/static/img/${game.cover}`;
                        img.alt = `Jaquette de ${game.title}`;
                        img.onerror = () => {
                            img.src = "/static/img/placeholder.png";
                        };

                        const title = document.createElement("h4");
                        title.textContent = game.title;

                        tile.appendChild(img);
                        tile.appendChild(title);
                        collectionGrid.appendChild(tile);
                    });
                }
            }
        })
        .catch(error => {
            // Génération d'un message d'erreur en cas...D'erreur.
            console.error(error);
            const errorMessage = document.getElementById('user-collection');
            if (errorMessage) {
                errorMessage.innerHTML = "<p>Impossible de charger le profil utilisateur...</p>";
            }
        });

    // Ceci permet de gérer la suppression de compte avec confirmation
    const deleteButton = document.getElementById('delete-btn');
    if (deleteButton) {
        deleteButton.addEventListener('click', () => {
            const confirmDelete = confirm("Êtes-vous sûr de vouloir supprimer votre profil ? Ceci est irréversible !");

            if (confirmDelete) {
                fetch('/api/delete_account', {
                    method: 'DELETE',
                    credentials: 'include'
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Erreur lors de la suppression du profil.");
                    }
                    return response.json();
                })
                .then(data => {
                    alert("Votre compte a bien été supprimé.");
                    localStorage.clear();
                    window.location.href = "/home";
                })
                .catch(error => {
                    console.error(error);
                    alert("Erreur : Impossible de supprimer votre profil.");
                });
            }
        });
    }
});
