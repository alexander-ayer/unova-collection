import os
import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host = "localhost",
        user="unova_app",
        password=os.environ["UNOVA_DB_PASSWORD"],
        database="unova_collection"
    )
    return connection