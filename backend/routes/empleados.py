from flask import Blueprint, jsonify, request
from db import get_db_connection

login_presidente_bp = Blueprint("login_presidente", __name__)

@login_presidente_bp.route("/", methods=["POST"])
def login_presidente():
    data = request.get_json()
    serie = data.get("serie")
    numero = data.get("numero")
    fecha = data.get("fecha")

    if not (serie and numero and fecha):
        return jsonify({"error": "Faltan parámetros"}), 400

    conn = get_db_connection()
    try:
        # Buscar ID de elección
        cursor1 = conn.cursor(dictionary=True, buffered=True)
        cursor1.execute("SELECT ID FROM Eleccion WHERE Fecha = %s;", (fecha,))
        eleccion = cursor1.fetchone()
        cursor1.close()
        if not eleccion:
            return jsonify({"error": "Elección no encontrada"}), 404

        id_eleccion = eleccion["ID"]

        # Buscar CI del ciudadano por credencial
        cursor2 = conn.cursor(dictionary=True, buffered=True)
        cursor2.execute("""
            SELECT CI_Ciudadano FROM Credencial
            WHERE serie = %s AND numero = %s
        """, (serie, numero))
        credencial = cursor2.fetchone()
        cursor2.close()
        if not credencial:
            return jsonify({"error": "Credencial no encontrada"}), 404

        ci = credencial["CI_Ciudadano"]

        # Buscar el tipo de empleado "Presidente"
        cursor3 = conn.cursor(dictionary=True, buffered=True)
        cursor3.execute("""
            SELECT ID FROM Tipo_Empleado WHERE Nombre = 'Presidente'
        """)
        tipo = cursor3.fetchone()
        cursor3.close()
        if not tipo:
            return jsonify({"error": "Tipo de empleado 'Presidente' no encontrado"}), 404

        id_tipo = tipo["ID"]

        # Buscar si el ciudadano es presidente de mesa en esa elección
        cursor4 = conn.cursor(dictionary=True, buffered=True)
        cursor4.execute("""
            SELECT ep.num_mesa
            FROM Empleado_Publico ep
            JOIN Mesa m ON ep.num_mesa = m.Num
            WHERE ep.CI_Ciudadano = %s AND ep.ID_tipo = %s AND m.ID_Eleccion = %s
        """, (ci, id_tipo, id_eleccion))
        presidente = cursor4.fetchone()
        cursor4.close()

        if presidente:
            return jsonify({"success": True, "mesa_id": presidente["num_mesa"]})
        else:
            return jsonify({"error": "No es presidente de mesa para esa elección"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()