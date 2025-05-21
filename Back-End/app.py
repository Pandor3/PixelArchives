from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Connexion à la base de données MySQL
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="FateIsTheBest",
    database="pixelarchives"
)

cursor = db.cursor()

# ROUTE DE TEST pour voir si l'API fonctionne =========================
@app.route('/')
def index():
    return " API PixelArchives connectée à MySQL"
#======================================================================

# ROUTE REGISTER pour enregistrer un nouvel utilisateur =======================================
@app.route('/register', methods=['POST'])
def register():

    #Lecture de la requête en JSON
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

# ROUTE LOGIN pour qu'utilisateur puisse s'identifier
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Les champs doivent être remplis'}), 400
    
    try:
        cursor.execute("""
                       SELECT password FROM users
                       WHERE username = %s
                       """, (username,))
        result = cursor.fetchone()

        if result and check_password_hash(result[0], password):
            return jsonify({'message': 'Connexion effectuée'}), 200
        else:
            return jsonify({'error': 'Identifiants invalides'}), 401
        
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
#======================================================

if __name__ == '__main__':
    app.run(debug=True)
