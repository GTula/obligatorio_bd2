from flask import Blueprint, jsonify, request
from db import get_db_connection

login_presidente_bp = Blueprint("login_presidente", __name__)

@login_presidente_bp.route("/login_presidente", methods=["POST"])
def login_presidente():
    data = request.get_json()
    serie = data.get("serie")
    numero = data.get("numero")
    fecha = data.get("fecha")

    if not (serie and numero and fecha):
        return jsonify({"error": "Faltan parámetros"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        # Buscar ID de elección
        cursor.execute("SELECT ID FROM Eleccion WHERE Fecha = %s;", (fecha,))
        eleccion = cursor.fetchone()
        if not eleccion:
            return jsonify({"error": "Elección no encontrada"}), 404

        id_eleccion = eleccion["ID"]

        # Verificar si es presidente
        cursor.execute("""
            SELECT p.ID_Mesa
            FROM Presidente p
            JOIN Ciudadano c ON p.serie_credencial = c.serie_credencial AND p.numero_credencial = c.numero_credencial
            WHERE p.serie_credencial = %s AND p.numero_credencial = %s AND p.ID_Eleccion = %s;
        """, (serie, numero, id_eleccion))
        presidente = cursor.fetchone()

        if presidente:
            return jsonify({"success": True, "mesa_id": presidente["ID_Mesa"]})
        else:
            return jsonify({"error": "Credencial inválida o no es presidente"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
