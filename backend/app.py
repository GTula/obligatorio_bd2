from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/api/ping")
def ping():
    return jsonify({"message": "pong"})

# Para pruebas de conexión con la base local
@app.route("/api/db")
def test_db():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "host.docker.internal"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "1117"),
        database=os.getenv("DB_NAME", "obligatorio"),
        port=int(os.getenv("DB_PORT", 3306))
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CIUDADANO;")
    result = cursor.fetchone()
    return jsonify({"CIUDADANO": result[3].isoformat()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
