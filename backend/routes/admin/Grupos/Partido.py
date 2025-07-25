
from flask import Blueprint, request, jsonify
from db import get_db_connection

partido_bp = Blueprint('partido', __name__)

# -------------------- Partido --------------------
@partido_bp.route('/partidos', methods=['GET'])
def listar_partidos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM partido")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@partido_bp.route('/partido', methods=['POST'])
def crear_partido():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO partido (nombre, direccion) VALUES (%s, %s)",
                   (data['nombre'], data['direccion']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Partido creado'})

@partido_bp.route('/partido/<int:id>', methods=['PUT'])
def modificar_partido(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE partido SET nombre = %s, direccion = %s WHERE id = %s",
                   (data['nombre'], data['direccion'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Partido modificado'})

@partido_bp.route('/partido/<int:id>', methods=['DELETE'])
def eliminar_partido(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM partido WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Partido eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar partido: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@partido_bp.route('/partido/forzar/<int:id>', methods=['DELETE'])
def forzar_eliminar_partido(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM autoridad WHERE id_partido = %s", (id,))
        cursor.execute("DELETE FROM lista WHERE id_partido = %s", (id,))
        cursor.execute("DELETE FROM partido WHERE id = %s", (id,))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Partido eliminado forzadamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
