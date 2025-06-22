from flask import Blueprint, jsonify, request
from db import get_db_connection

eleccion_bp = Blueprint("eleccion", __name__)

@eleccion_bp.route("/", methods=["GET"])
def get_eleccion_por_fecha():
    fecha = request.args.get("fecha")
    if not fecha:
        return jsonify({"error": "Falta el parámetro 'fecha'"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute("SELECT * FROM eleccion WHERE fecha = %s;", (fecha,))
        eleccion = cursor.fetchall()
        if eleccion:
            return jsonify(eleccion)
        return jsonify({"error": "Elección no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()