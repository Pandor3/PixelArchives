from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
load_dotenv()

# Connexion à la base de données MySQL
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()

# ROUTE DE TEST pour voir si l'API fonctionne =========================
@app.route('/')
def index():
    return " API PixelArchives connectée à MySQL"
#======================================================================

# ROUTE REGISTER pour enregistrer un nouvel utilisateur ===============
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

        # Requête SQL envoyée à la base de données (database) avec les données utilisateur
        cursor.execute("""
                       INSERT INTO users(username, email, password)
                       VALUES (%s, %s, %s)
                       """, (username, email, hashed_password))
        db.commit()

        # Retour attendu en cas de succès
        return jsonify({'message': f'Utilisateur {username} créé avec succès.'})
    
    # Code d'erreur renvoyé en cas d'échec
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
#=================================================================================================

# ROUTE LOGIN pour que l'utilisateur puisse s'identifier
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
                       SELECT password FROM users
                       WHERE username = %s
                       """, (username,))
        result = cursor.fetchone()

        # Retour attendus
        if result and check_password_hash(result[0], password):
            # Retour positif
            return jsonify({'message': 'Connexion effectuée'}), 200
        else:
            # Retour négatif si les identifiants ne correspondent pas aux données attendues
            return jsonify({'error': 'Identifiants invalides'}), 401
        
    # Message d'erreur en cas de problème serveur (500)    
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
#==============================================================================================

if __name__ == '__main__':
    app.run(debug=True)
