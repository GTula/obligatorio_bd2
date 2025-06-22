
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

@mesa_bp.route('', methods=['POST'])
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

@mesa_bp.route('/<int:num>', methods=['PUT'])
def modificar_mesa(num):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE mesa SET id_circuito = %s, id_eleccion = %s WHERE num = %s",
                   (data['id_circuito'], data['id_eleccion'], num))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Mesa modificada'})

@mesa_bp.route('/<int:num>', methods=['DELETE'])
def eliminar_mesa(num):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM mesa WHERE num = %s", (num,))
        conn.commit()
        return jsonify({'mensaje': 'Mesa eliminada'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar mesa: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()



