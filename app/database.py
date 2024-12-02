import mysql.connector

def connect_to_db():
    conn= mysql.connector.connect(
        host="localhost",    
        user="root", 
        password="root", 
        database="retail_db" 
    )
    cursor = conn.cursor()
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")  # Disabling safe update for this session
    return conn
