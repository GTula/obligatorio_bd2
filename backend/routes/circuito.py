from flask import Blueprint, jsonify, request
from db import get_db_connection

circuito_bp = Blueprint("circuito", __name__)

@circuito_bp.route("/", methods=["GET"])
def get_circuito_por_credencial():
    serie = request.args.get("serie")
    numero = request.args.get("numero")
    fecha = request.args.get("fecha")
    print(f"Parámetros recibidos: serie={serie}, numero={numero}, fecha={fecha}")
    
    if not (serie and numero and fecha):
        return jsonify({"error": "Faltan parámetros: serie, numero o fecha"}), 400

    conn = get_db_connection()
    try:
        # Primer cursor con buffered
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT ID FROM Eleccion WHERE Fecha = %s;", (fecha,))
        eleccion = cursor.fetchone()
        cursor.close()

        if not eleccion:
            return jsonify({"error": "No se encontró una elección para esa fecha"}), 404

        id_eleccion = eleccion["ID"]
        print(f"ID de elección encontrado: {id_eleccion}")

        # Segundo cursor con buffered
        cursor2 = conn.cursor(dictionary=True, buffered=True)
        cursor2.execute("""
            SELECT a.ID_circuito, a.ID_eleccion
            FROM Asignado a
            WHERE a.serie_credencial = %s AND a.numero_credencial = %s AND a.ID_eleccion = %s;
        """, (serie, numero, id_eleccion))
        circuito = cursor2.fetchone()
        cursor2.close()

        if circuito:
            return jsonify(circuito)
        return jsonify({"error": "No se encontró circuito para esa credencial y elección"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
