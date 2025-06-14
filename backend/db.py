import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "host.docker.internal"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "1117"),
        database=os.getenv("DB_NAME", "obligatorio"),
        port=int(os.getenv("DB_PORT", 3306))
    )