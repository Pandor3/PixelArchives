from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    print("Connexion à MySQL réussie!")
    db.close()

except mysql.connector.Error as err:
    print("Erreur de connexion :", err)
