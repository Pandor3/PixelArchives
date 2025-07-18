document.addEventListener("DOMContentLoaded", () => {
    // Ceci récupère le formulaire de connexion et les erreurs de Login
    const loginForm = document.getElementById("loginForm");

    loginForm.addEventListener("submit", async (e) => {
        // Ceci empêche le rechargement de la page avant que les informations ne soient récupérées
        e.preventDefault();

        // Ceci récupère les valeurs saisies par l'utilisateur sur la page de login
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        try {
            // Ceci envoie une requête POST vers la route login de l'API sous format JSON
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, password })
            });

            // Ceci permet de récupérer la réponse en JSON du serveur
            const result = await response.json();

            // En cas de réponse positive...
            if (response.ok) {
                // On stocke le token JWT dans le navigateur en local
                localStorage.setItem("jwt", result.token);
                // On redirige l'utilisateur vers la page d'accueil
                window.location.href = "/home";
            } else {
                // En cas d'erreur, un message...D'erreur apparait
                alert(result.error || "Identifiant ou mot de passe incorrect !");
            }
        } catch (err) {
            // En cas d'erreur réseau
            alert("Erreur de connexion au serveur !")
        }
    });
});
