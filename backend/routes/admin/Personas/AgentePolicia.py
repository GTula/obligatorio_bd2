
from flask import Blueprint, request, jsonify
from db import get_db_connection

agente_policia_bp = Blueprint('agente-policia', __name__)


# -------------------- Agente Policía --------------------
@agente_policia_bp.route('/agentes-policia', methods=['GET'])
def listar_agentes_policia():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agente_policia")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@agente_policia_bp.route('/agente-policia', methods=['POST'])
def crear_agente_policia():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO agente_policia (ci_ciudadano, id_comisaria) VALUES (%s, %s)",
                   (data['ci_ciudadano'], data['id_comisaria']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Agente de policía creado'})

@agente_policia_bp.route('/agente-policia/<ci>', methods=['PUT'])
def modificar_agente_policia(ci):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE agente_policia SET id_comisaria = %s WHERE ci_ciudadano = %s",
                   (data['id_comisaria'], ci))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Agente de policía modificado'})

@agente_policia_bp.route('/agente-policia/<ci>', methods=['DELETE'])
def eliminar_agente_policia(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM agente_policia WHERE ci_ciudadano = %s", (ci,))
        conn.commit()
        return jsonify({'mensaje': 'Agente de policía eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar agente de policía: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@agente_policia_bp.route('/agente-policia/forzar/<ci_ciudadano>', methods=['DELETE'])
def forzar_eliminar_agente_policia(ci_ciudadano):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM agente_establecimiento WHERE ci_policia = %s", (ci_ciudadano,))
        cursor.execute("DELETE FROM agente_policia WHERE ci_ciudadano = %s", (ci_ciudadano,))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Agente de policía eliminado forzadamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
