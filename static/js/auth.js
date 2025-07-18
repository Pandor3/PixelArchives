document.addEventListener("DOMContentLoaded", () => {
    // Ceci permet de récupérer le token JWT de l'utilisateur connecté
    const token = localStorage.getItem("jwt");

    // Ceci permet de récupérer chaque élément des headers par son ID
    const loginItem = document.getElementById("btn-login");
    const registerItem = document.getElementById("btn-register");
    const forumItem = document.getElementById("btn-forum");
    const logoutItem = document.getElementById("btn-logout");
    const profilItem = document.getElementById("btn-profil");

    // Si l'utilisateur est connecté...
    if (token) {
        // Ceci masque les liens de connexion et de création de compte
        if (loginItem) loginItem.style.display = "none";
        if (registerItem) registerItem.style.display = "none";
        // Ceci affiche les liens menant au forum, la déconnexion et le profil de l'utilisateur connecté
        if (forumItem) forumItem.style.display = "list-item";
        if (logoutItem) logoutItem.style.display = "list-item";
        if(profilItem) profilItem.style.display = "list-item";
    } else {
        // Si l'utilisateur n'est pas connecté...
        // Ceci affiche les liens de connexion et de création de compte
        if (loginItem) loginItem.style.display = "list-item";
        if (registerItem) registerItem.style.display = "list-item";
        // Ceci masque les liens vers le forum, la déconnexion et le profil
        if (forumItem) forumItem.style.display = "none";
        if (logoutItem) logoutItem.style.display = "none";
        if (profilItem) profilItem.style.display = "none";
    }
});

// Ceci déconnectera l'utilisateur, enlèvera le token JWT (les droits d'accès) et rafraîchira la page lorsqu'il cliquera sur "Déconnexion"
function logout() {
    localStorage.removeItem("jwt");
    window.location.href = "/logout";
}
