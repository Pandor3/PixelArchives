document.addEventListener("DOMContentLoaded", () => {
    // Ceci permet de sélectionner le formulaire d'inscription
    const form = document.querySelector(".RegisterForm");

    // Interception de la soumission du formulaire en HTML
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Ceci permet de récupérer les valeurs saisies dans le formulaire de la page d'inscription.
        const username = document.querySelector("input[name='Username']").value;
        const email = document.querySelector("input[name='Email']").value;
        const password = document.querySelector("input[name='Password']").value;
        const confirmPassword = document.querySelector("input[name='ConfirmPassword']").value;

        // Ceci permet de vérifier que les deux mots de passes sont identiques
        if (password !== confirmPassword) {
            alert("Les mots de passe ne correspondent pas !");
            return;
        }

        try {
            // Ceci permet d'envoyer la requête POST vers l'API avec les donnée saisies
            const response = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email, password })
            });

            // On attend de récupérer la réponse en JSON
            const result = await response.json();

            // Si la réponse est positive...
            if (response.ok) {
                // Un message de confirmation + redirection vers la page de connexion
                alert("Inscription réussie.");
                window.location.href = "/connexion";
            } else {
                // Sinon un message d'erreur
                alert(result.error || "Erreur lors de l'inscription");
            }
        } catch (err) {
            // En cas de requête échouée si il y'a une erreur réseau
            alert("Erreur serveur : Impossible de contacter l'API.");
        }
    });
});
