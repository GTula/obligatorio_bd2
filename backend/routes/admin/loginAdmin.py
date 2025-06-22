from flask import Blueprint, request, jsonify
from db import get_db_connection
import bcrypt

login_admin_bp = Blueprint("login_admin", __name__)

@login_admin_bp.route("/", methods=["POST"])
def login_admin():
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")

    if not usuario or not password:
        return jsonify({"error": "Faltan campos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute("SELECT password FROM administrador WHERE usuario = %s", (usuario,))
        admin = cursor.fetchone()
        if not admin:
            return jsonify({"error": "Usuario no encontrado"}), 404

        password_hash = admin["password"]

        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return jsonify({"success": True, "message": "Login exitoso"})
        else:
            return jsonify({"error": "Contraseña incorrecta"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

