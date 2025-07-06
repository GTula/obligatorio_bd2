
from flask import Blueprint, request, jsonify
from db import get_db_connection

mesa_bp = Blueprint('mesa', __name__)

# -------------------- Mesa --------------------
@mesa_bp.route('/mesas', methods=['GET'])
def listar_mesas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mesa")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@mesa_bp.route('/mesa', methods=['POST'])
def crear_mesa():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mesa (num, id_circuito, id_eleccion) VALUES (%s, %s, %s)",
                   (data['num'], data['id_circuito'], data['id_eleccion']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Mesa creada'})

@mesa_bp.route('/mesa/<int:num>/<int:id_circuito>/<int:id_eleccion>', methods=['PUT'])
def modificar_mesa(num, id_circuito, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE mesa SET id_circuito = %s, id_eleccion = %s WHERE num = %s AND id_circuito = %s AND id_eleccion = %s",
                       (data['id_circuito'], data['id_eleccion'], num, id_circuito, id_eleccion))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Mesa no encontrada'}), 404
        conn.commit()
        return jsonify({'mensaje': 'Mesa modificada'})
    except Exception as e:
        return jsonify({'error': f'Error modificando mesa: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()

@mesa_bp.route('/mesa/<int:num>/<int:id_circuito>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_mesa(num, id_circuito, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM mesa WHERE num = %s AND id_circuito = %s AND id_eleccion = %s", 
                       (num, id_circuito, id_eleccion))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Mesa no encontrada'}), 404
        conn.commit()
        return jsonify({'mensaje': 'Mesa eliminada'})
    except Exception as e:
        return jsonify({'error': f'Error eliminando mesa: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()

@mesa_bp.route('/mesa/forzar/<int:num>/<int:id_circuito>/<int:id_eleccion>', methods=['DELETE'])
def forzar_eliminar_mesa(num, id_circuito, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM participacion_en_mesa WHERE num_mesa = %s AND id_circuito = %s AND id_eleccion = %s", (num, id_circuito, id_eleccion))
        cursor.execute("DELETE FROM mesa WHERE num = %s AND id_circuito = %s AND id_eleccion = %s", (num, id_circuito, id_eleccion))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Mesa eliminada forzadamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()


