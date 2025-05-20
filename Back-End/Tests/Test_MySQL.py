import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="FateIsTheBest",
    )
    print("Connexion à MySQL réussie!")
    db.close()

except mysql.connector.Error as err:
    print("Erreur de connexion :", err)
