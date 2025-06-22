from flask import Blueprint, jsonify, request
from db import get_db_connection

ciudadanos_bp = Blueprint("ciudadanos", __name__)

@ciudadanos_bp.route("/", methods=["GET"])
def get_ciudadanos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ciudadano;")
    ciudadanos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(ciudadanos)

@ciudadanos_bp.route("/<ci>", methods=["GET"])
def get_ciudadano(ci):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ciudadano WHERE ci = %s;", (ci,))
    ciudadano = cursor.fetchone()
    cursor.close()
    conn.close()
    if ciudadano:
        return jsonify(ciudadano)
    return jsonify({"error": "ciudadano no encontrado"}), 404

def validar_ci_uruguaya(ci):
    """Valida la cédula uruguaya usando el dígito verificador."""
    ci = ci.zfill(8)
    if not ci.isdigit() or len(ci) != 8:
        return False
    coef = [2, 9, 8, 7, 6, 3, 4]
    suma = sum([int(ci[i]) * coef[i] for i in range(7)])
    dv = ((10 - (suma % 10)) % 10)
    return dv == int(ci[7])

@ciudadanos_bp.route("/", methods=["POST"])
def create_ciudadano():
    data = request.json
    ci = data.get("ci", "")
    if not validar_ci_uruguaya(ci):
        return jsonify({"error": "Cédula inválida"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO ciudadano (ci, nombre, apellido, fecha_nac) VALUES (%s, %s, %s, %s);",
            (ci, data["nombre"], data["apellido"], data["fecha_nac"])
        )
        conn.commit()
        return jsonify({"message": "ciudadano creado"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@ciudadanos_bp.route("/<ci>", methods=["PUT"])
def update_ciudadano(ci):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE ciudadano SET nombre=%s, apellido=%s, fecha_nac=%s WHERE ci=%s;",
            (data["nombre"], data["apellido"], data["fecha_nac"], ci)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "ciudadano no encontrado"}), 404
        return jsonify({"message": "ciudadano actualizado"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@ciudadanos_bp.route("/<ci>", methods=["DELETE"])
def delete_ciudadano(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ciudadano WHERE ci=%s;", (ci,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "ciudadano no encontrado"}), 404
        return jsonify({"message": "ciudadano eliminado"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()