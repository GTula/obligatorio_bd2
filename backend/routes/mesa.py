from flask import Blueprint, jsonify, request
from db import get_db_connection

mesa_bp = Blueprint("mesa", __name__)

@mesa_bp.route('/<int:num>/<int:id_circuito>/<int:id_eleccion>', methods=['PUT'])
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

@mesa_bp.route('/<int:num>/<int:id_circuito>/<int:id_eleccion>', methods=['DELETE'])
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

