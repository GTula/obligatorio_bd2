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
        # Buscar id de elección
        cursor1 = conn.cursor(dictionary=True, buffered=True)
        cursor1.execute("SELECT id FROM eleccion WHERE fecha = %s;", (fecha,))
        eleccion = cursor1.fetchone()
        cursor1.close()
        if not eleccion:
            return jsonify({"error": "Elección no encontrada"}), 404

        id_eleccion = eleccion["id"]

        # Buscar ci del ciudadano por credencial
        cursor2 = conn.cursor(dictionary=True, buffered=True)
        cursor2.execute("""
            SELECT ci_ciudadano FROM credencial
            WHERE serie = %s AND numero = %s
        """, (serie, numero))
        credencial = cursor2.fetchone()
        cursor2.close()
        if not credencial:
            return jsonify({"error": "Credencial no encontrada"}), 404

        ci = credencial["ci_ciudadano"]

        # Buscar el tipo de empleado "Presidente"
        cursor3 = conn.cursor(dictionary=True, buffered=True)
        cursor3.execute("""
            SELECT id FROM tipo_empleado WHERE nombre = 'Presidente'
        """)
        tipo = cursor3.fetchone()
        cursor3.close()
        if not tipo:
            return jsonify({"error": "Tipo de empleado 'Presidente' no encontrado"}), 404

        id_tipo = tipo["id"]

        # Buscar si el ciudadano es presidente de mesa en esa elección
        cursor4 = conn.cursor(dictionary=True, buffered=True)
        cursor4.execute("""
            SELECT pm.num_mesa
            FROM participacion_en_mesa pm
            JOIN empleado_publico ep ON pm.ci_ciudadano = ep.ci_ciudadano
            WHERE ep.ci_ciudadano = %s AND pm.id_tipo = %s AND pm.id_eleccion = %s
        """, (ci, id_tipo, id_eleccion))
        presidente = cursor4.fetchone()
        cursor4.close()

        if presidente:
            return jsonify({
                "success": True, 
                "mesa_id": presidente["num_mesa"],
                "id_eleccion": id_eleccion
            })
        else:
            return jsonify({"error": "No es presidente de mesa para esa elección"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()