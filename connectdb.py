import mysql.connector

#Connect With Database
def connect():
    user_db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "lolxd420",
        database = "emp"
    )
    return user_db

#Close Connection
def disconnect(db):
    db.close()