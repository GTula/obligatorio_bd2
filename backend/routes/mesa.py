from flask import Blueprint, jsonify, request
from db import get_db_connection

mesa_bp = Blueprint("mesa", __name__)

@mesa_bp.route("/", methods=["GET"])
def get_mesa_empleado():
    ci = request.args.get("ci")
    fecha = request.args.get("fecha")
    if not (ci and fecha):
        return jsonify({"error": "Faltan parámetros: ci o fecha"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)  # <- BUFFERED agregado

    try:
        # Buscar el id de la elección por fecha
        cursor.execute("SELECT id FROM eleccion WHERE fecha = %s;", (fecha,))
        eleccion = cursor.fetchone()
        if not eleccion:
            return jsonify({"error": "No se encontró una elección para esa fecha"}), 404

        id_eleccion = eleccion["id"]

        # Buscar la mesa del empleado público para esa elección
        cursor.execute("""
            SELECT m.num, m.id_circuito, m.id_eleccion
            FROM empleado_Publico ep
            JOIN mesa m ON ep.num_mesa = m.num
            WHERE ep.ci_ciudadano = %s AND m.id_eleccion = %s;
        """, (ci, id_eleccion))
        mesa = cursor.fetchone()

        if mesa:
            return jsonify(mesa)
        return jsonify({"error": "No se encontró mesa para ese empleado público y elección"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@mesa_bp.route("/info", methods=["GET"])
def get_mesa_info():
    num_mesa = request.args.get("num_mesa")
    fecha = request.args.get("fecha")
    
    if not (num_mesa and fecha):
        return jsonify({"error": "Faltan parámetros: num_mesa o fecha"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        # Buscar el id de la elección por fecha
        cursor.execute("SELECT id FROM eleccion WHERE fecha = %s;", (fecha,))
        eleccion = cursor.fetchone()
        if not eleccion:
            return jsonify({"error": "No se encontró una elección para esa fecha"}), 404

        id_eleccion = eleccion["id"]

        # Obtener información de la mesa y circuito
        cursor.execute("""
            SELECT m.num as num_mesa, m.id_circuito, c.num as num_circuito,
                   (SELECT COUNT(*) FROM asignado a 
                    WHERE a.id_circuito = m.id_circuito 
                    AND a.id_eleccion = m.id_eleccion) as total_votantes
            FROM mesa m
            JOIN circuito c ON m.id_circuito = c.id
            WHERE m.num = %s AND m.id_eleccion = %s;
        """, (num_mesa, id_eleccion))
        
        mesa_info = cursor.fetchone()
        if mesa_info:
            return jsonify(mesa_info)
        return jsonify({"error": "No se encontró información para esa mesa y elección"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
