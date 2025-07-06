
from flask import Blueprint, request, jsonify
from db import get_db_connection

autoridad_bp = Blueprint('autoridad', __name__)


# -------------------- Autoridad --------------------
@autoridad_bp.route('/autoridades', methods=['GET'])
def listar_autoridades():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM autoridad")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@autoridad_bp.route('/autoridad', methods=['POST'])
def crear_autoridad():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO autoridad (ci_ciudadano, id_partido) VALUES (%s, %s)",
                   (data['ci_ciudadano'], data['id_partido']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Autoridad creada'})

@autoridad_bp.route('/autoridad/<ci>', methods=['PUT'])
def modificar_autoridad(ci):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE autoridad SET id_partido = %s WHERE ci_ciudadano = %s",
                   (data['id_partido'], ci))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Autoridad modificada'})

@autoridad_bp.route('/autoridad/<ci>', methods=['DELETE'])
def eliminar_autoridad(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM autoridad WHERE ci_ciudadano = %s", (ci,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Autoridad eliminada'})

@autoridad_bp.route('/autoridad/forzar/<ci_ciudadano>', methods=['DELETE'])
def forzar_eliminar_autoridad(ci_ciudadano):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM autoridad WHERE ci_ciudadano = %s", (ci_ciudadano,))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Autoridad eliminada forzadamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
