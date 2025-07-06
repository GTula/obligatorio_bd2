
from flask import Blueprint, request, jsonify
from db import get_db_connection

agente_establecimiento_bp = Blueprint('agente-establecimiento', __name__)


# -------------------- Agente Establecimiento --------------------
@agente_establecimiento_bp.route('/agentes-establecimiento', methods=['GET'])
def listar_agentes_establecimiento():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agente_establecimiento")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@agente_establecimiento_bp.route('/agente-establecimiento', methods=['POST'])
def crear_agente_establecimiento():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO agente_establecimiento (ci_policia, id_establecimiento) VALUES (%s, %s)",
                   (data['ci_policia'], data['id_establecimiento']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Agente establecimiento creado'})

@agente_establecimiento_bp.route('/agente-establecimiento/<ci>/<int:id_establecimiento>', methods=['PUT'])
def modificar_agente_establecimiento(ci, id_establecimiento):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE agente_establecimiento SET id_establecimiento = %s WHERE ci_policia = %s AND id_establecimiento = %s",
                   (data['id_establecimiento'], ci, id_establecimiento))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Agente establecimiento modificado'})

@agente_establecimiento_bp.route('/agente-establecimiento/<ci>/<int:id_establecimiento>', methods=['DELETE'])
def eliminar_agente_establecimiento(ci, id_establecimiento):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agente_establecimiento WHERE ci_policia = %s AND id_establecimiento = %s",
                   (ci, id_establecimiento))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Agente establecimiento eliminado'})

@agente_establecimiento_bp.route('/agente-establecimiento/forzar/<ci_policia>/<int:id_establecimiento>', methods=['DELETE'])
def forzar_eliminar_agente_establecimiento(ci_policia, id_establecimiento):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM agente_establecimiento WHERE ci_policia = %s AND id_establecimiento = %s", (ci_policia, id_establecimiento))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Agente establecimiento eliminado forzadamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
