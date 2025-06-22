import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", " mysql.reto-ucu.net"),
        user=os.getenv("DB_USER", "ic_g7_admin"),
        password=os.getenv("DB_PASSWORD", "Bd2025!"),
        database=os.getenv("DB_NAME", "IC_Grupo7"),
        port=int(os.getenv("DB_PORT", 50006))
    )