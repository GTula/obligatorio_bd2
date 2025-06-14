from flask import Blueprint, jsonify, request
from db import get_db_connection

ciudadanos_bp = Blueprint("ciudadanos", __name__)

@ciudadanos_bp.route("/", methods=["GET"])
def get_ciudadanos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Ciudadano;")
    ciudadanos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(ciudadanos)

@ciudadanos_bp.route("/<ci>", methods=["GET"])
def get_ciudadano(ci):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Ciudadano WHERE CI = %s;", (ci,))
    ciudadano = cursor.fetchone()
    cursor.close()
    conn.close()
    if ciudadano:
        return jsonify(ciudadano)
    return jsonify({"error": "Ciudadano no encontrado"}), 404

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
    ci = data.get("CI", "")
    if not validar_ci_uruguaya(ci):
        return jsonify({"error": "Cédula inválida"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Ciudadano (CI, nombre, apellido, Fecha_nac) VALUES (%s, %s, %s, %s);",
            (ci, data["nombre"], data["apellido"], data["Fecha_nac"])
        )
        conn.commit()
        return jsonify({"message": "Ciudadano creado"}), 201
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
            "UPDATE Ciudadano SET nombre=%s, apellido=%s, Fecha_nac=%s WHERE CI=%s;",
            (data["nombre"], data["apellido"], data["Fecha_nac"], ci)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Ciudadano no encontrado"}), 404
        return jsonify({"message": "Ciudadano actualizado"})
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
        cursor.execute("DELETE FROM Ciudadano WHERE CI=%s;", (ci,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Ciudadano no encontrado"}), 404
        return jsonify({"message": "Ciudadano eliminado"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()