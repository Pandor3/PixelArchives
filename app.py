from dotenv import load_dotenv
import os
import json
from flask import Flask, request, jsonify, render_template
import mysql.connector
import uuid
import jwt
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
load_dotenv()

# Connexion à la base de données MySQL
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

cursor = db.cursor()

# ROUTES DE TEST pour voir si l'API fonctionne =========================
@app.route('/')
def index():
    return " API PixelArchives connectée à MySQL"

# Route HTML de l'accueil visuel
@app.route('/home')
def home_page():
    return render_template('index.html')

# Page d'inscription HTML
@app.route('/inscription')
def register_page():
    return render_template('register.html')

# Page de login HTML
@app.route('/connexion')
def login_page():
    return render_template('login.html')

# Page du forum
@app.route('/hub')
def hub_page():
    return render_template('hub.html')

# Page Minidex dynamique
@app.route('/minidex')
def minidex():
    return render_template('minidex.html')
#======================================================================

# ROUTE /REGISTER pour enregistrer un nouvel utilisateur ===============
@app.route('/register', methods=['POST'])
def register():

    # Lecture de la requête en JSON
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Condition d'erreur si l'utilisateur ne remplit pas tout les champs
    if not username or not email or not password:
        return jsonify({'error': 'Les champs username, email et password sont requis'}), 400
    
    try:
        # Hachage du mot de passe pour plus de sécurité
        hashed_password = generate_password_hash(password)

        # Génération d'un UUID dans la base de données
        new_uuid = str(uuid.uuid4())

        # Requête SQL envoyée à la base de données (database) avec les données utilisateur
        cursor.execute("""
                       INSERT INTO users(uuid, username, email, password)
                       VALUES (%s, %s, %s, %s)
                       """, (new_uuid, username, email, hashed_password))
        db.commit()

        # Retour attendu en cas de succès
        return jsonify({'message': f'Utilisateur {username} créé avec succès.'})
    
    # Code d'erreur renvoyé en cas d'échec
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
#=================================================================================================

# ROUTE /LOGIN pour que l'utilisateur puisse s'identifier =========================================
@app.route('/login', methods=['POST'])
def login():

    # Lecture de la requête en JSON
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    
    # Message d'erreur au cas où l'utilisateur ne remplis pas tout les champs
    if not username or not password:
        return jsonify({'error': 'Les champs doivent être remplis'}), 400
    
    try:

        # Requête envoyée à la base de données MySQL pour tenter de trouver le mot de passe correspondant
        cursor.execute("""
                       SELECT uuid, password FROM users
                       WHERE username = %s
                       """, (username,))
        result = cursor.fetchone()

        # Retour attendus
        if result and check_password_hash(result[1], password):
            user_uuid = result[0]

            # Création du JWT
            token = jwt.encode({
                'uuid': user_uuid,
                'exp': datetime.now(timezone.utc) + timedelta(hours=2)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            # Retour positif, un JWT est donné à l'utilisateur lors de sa connexion
            return jsonify({'message': 'Connexion effectuée', 'token': token}), 200
        else:
            # Retour négatif si les identifiants ne correspondent pas aux données attendues
            return jsonify({'error': 'Identifiants invalides'}), 401
        
    # Message d'erreur en cas de problème serveur (500)    
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
#==============================================================================================

# ROUTE /API/GAMES pour la génération des jeux depuis la BDD =========================================
@app.route('/api/games')
def api_games():
    try:
        cursor.execute("SELECT id, title, console, year, genre, cover FROM games")
        rows = cursor.fetchall()
        games = [
            {
                'id': row[0],
                'title': row[1],
                'console': row[2],
                'year': row[3],
                'genre': row[4],
                'cover': row[5]
            } for row in rows
        ]
        return jsonify(games)
    except mysql.connector.Error as err:
        return jsonify({'error' :str(err)}), 500
#==============================================================================================

if __name__ == '__main__':
    app.run(debug=True)
