from flask import Flask, request, jsonify
import mysql.connector

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

@app.route('/')
def index():
    return " API PixelArchives connectée à MySQL"

if __name__ == '__main__':
    app.run(debug=True)
