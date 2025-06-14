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
        # Buscar el ID de la elección por fecha
        cursor.execute("SELECT ID FROM Eleccion WHERE Fecha = %s;", (fecha,))
        eleccion = cursor.fetchone()
        if not eleccion:
            return jsonify({"error": "No se encontró una elección para esa fecha"}), 404

        id_eleccion = eleccion["ID"]

        # Buscar la mesa del empleado público para esa elección
        cursor.execute("""
            SELECT m.Num, m.ID_Circuito, m.ID_Eleccion
            FROM Empleado_Publico ep
            JOIN Mesa m ON ep.num_mesa = m.Num
            WHERE ep.CI_Ciudadano = %s AND m.ID_Eleccion = %s;
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
