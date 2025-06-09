from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

@app.route("/api/ping")
def ping():
    return jsonify({"message": "pong"})

# Para pruebas de conexión con la base local
@app.route("/api/db")
def test_db():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "host.docker.internal"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "votacion_db")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW()")
    result = cursor.fetchone()
    return jsonify({"now": result[0].isoformat()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
