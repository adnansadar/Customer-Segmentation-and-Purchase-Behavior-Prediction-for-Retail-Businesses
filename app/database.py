import mysql.connector
from dotenv import load_dotenv
import os

def connect_to_db():
    conn= mysql.connector.connect(
       host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")  # Disabling safe update for this session
    return conn
