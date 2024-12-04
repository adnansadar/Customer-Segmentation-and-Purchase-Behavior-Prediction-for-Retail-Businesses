import mysql.connector
from dotenv import load_dotenv
import os


def connect_to_db():
    conn= mysql.connector.connect(
        host=os.environ.get("DB_HOST"), 
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port =int(os.environ.get("DB_PORT"))
    )
    cursor = conn.cursor()
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")  # Disabling safe update for this session
    return conn
