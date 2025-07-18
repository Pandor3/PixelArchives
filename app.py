from dotenv import load_dotenv
import os
import json
from flask import Flask, request, jsonify, render_template, redirect
import mysql.connector
from mysql.connector import Error
import time
import uuid
import jwt
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
load_dotenv()

# Connexion à la base de données MySQL en 10 tentatives (afin que Docker charge bien le SQL)
attempts = 10
while attempts > 0:
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        print("Connexion à la base de données réussie !")
        break
    except Error as err:
        print(f"En attente de la base de données... ({10 - attempts + 1}/10)")
        print(err)
        attempts -= 1
        time.sleep(3)

if attempts == 0:
    raise Exception("Impossible de se connecter à la base de données après 10 tentatives.")

cursor = db.cursor()

# ROUTES pour accéder au HTML =========================
@app.route('/')
def index():
    return '''
        <h1>API PixelArchives connectée à MySQL</h1>
        <p><a href="/home">Accéder à l'accueil</a></p>
    '''

# Route HTML de l'accueil visuel
@app.route('/home')
def home_page():
    return render_template('index.html')

# Page d'inscription
@app.route('/inscription')
def register_page():
    return render_template('register.html')

# Page de connexion
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

# Page de profil utilisateur
@app.route('/profil')
def profil():
    token = request.cookies.get('jwt')
    if not token:
        return redirect('/connexion')
    
    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return render_template('profil.html')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return redirect('/connexion')
    
# Route de déconnexion
@app.route('/logout')
def logout():
    response = redirect('/home')
    response.set_cookie('jwt', '', expires=0)
    return response
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

            # Création du JWT et de sa durée avant expiration
            token = jwt.encode({
                'uuid': user_uuid,
                'exp': datetime.now(timezone.utc) + timedelta(hours=2)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            # Retour positif, un JWT est donné à l'utilisateur lors de sa connexion
            response = jsonify({'message': 'Connexion effectuée'})
            response.set_cookie('jwt', token, httponly=True, samesite='Strict')
            return response, 200
        else:
            # Retour négatif si les identifiants ne correspondent pas aux données attendues
            return jsonify({'error': 'Identifiants invalides'}), 401
        
    # Message d'erreur en cas de problème serveur (500)    
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
#==============================================================================================

# ROUTE /API/PROFIL pour accéder au JSON du profil utilisateur actuel =========================================
@app.route('/api/profil', methods=['GET'])
def get_profile():
    token = request.cookies.get('jwt')
    if not token:
        return jsonify({'error': 'Token manquant'}), 401
    
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_uuid = decoded_token.get('uuid')

        cursor.execute("""
            SELECT username, email, created_at
            FROM users
            WHERE uuid = %s
        """, (user_uuid,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'Utilisateur introuvable'}), 404

        # On récupère à la fois id, title, cover pour l'affichage sur le profil
        cursor.execute("""
            SELECT g.id, g.title, g.cover
            FROM users_games ug
            JOIN games g ON ug.game_id = g.id
            WHERE ug.user_uuid = %s
            ORDER BY ug.added_at DESC
        """, (user_uuid,))
        collection = cursor.fetchall()

        return jsonify({
            'username': user[0],
            'email': user[1],
            'created_at': str(user[2]),
            'collection': [
                {
                    'id': row[0],
                    'title': row[1],
                    'cover': row[2]
                } for row in collection
            ]
        }), 200
    
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expiré'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error' : 'Token invalide'}), 401

#==============================================================================================

# ROUTE /API/USERS/ADD_GAME pour ajouter les jeux sur les profils utilisateurs =========================================
@app.route('/api/users/add_game', methods=['POST'])
def add_game_to_user():
    token = request.cookies.get('jwt')
    if not token:
        return jsonify({'error': 'Token manquant'}), 401
    
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_uuid = decoded.get('uuid')

        data = request.get_json()
        game_id = data.get('game_id')

        if not game_id:
            return jsonify({'error': 'game_id manquant'}), 400
        
        # Ceci va ajouter le lien entre l'utilisateur et le jeu dans la table associative
        cursor.execute("""
            INSERT IGNORE INTO users_games (user_uuid, game_id)
            VALUES (%s, %s)                       
        """, (user_uuid, game_id))
        db.commit()

        return jsonify({'message': 'Jeu ajouté avec succès à votre collection !'}), 201
    
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expiré'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token invalide'}), 401
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
#==============================================================================================

# ROUTE /API/GAMES pour la génération des cartes de jeux depuis la BDD =========================================
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

# ROUTE /API/DELETE_ACCOUNT pour supprimer un compte utilisateur =========================================
@app.route('/api/delete_account', methods=['DELETE'])
def delete_account():
    token = request.cookies.get('jwt')
    if not token:
        return jsonify({'error': 'Token manquant'}), 401
    
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_uuid = decoded_token.get('uuid')

        # Ceci va supprimer les jeux liés dans users_games
        cursor.execute("DELETE FROM users_games WHERE user_uuid = %s", (user_uuid,))

        # Ceci va supprimer l'utilisateur une fois les jeux supprimés de sa collection
        cursor.execute("DELETE FROM users WHERE uuid = %s", (user_uuid,))
        db.commit()

        # Ceci va montrer les diverses réponses que l'utilisateur recevra
        response = jsonify({'message': 'Compte supprimé'})
        response.set_cookie('jwt', '', expires=0)
        return response, 200
    
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expiré'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token invalide'}), 401
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

#==============================================================================================

if __name__ == '__main__':
    app.run(debug=True)
