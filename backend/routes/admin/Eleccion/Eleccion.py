
from flask import Blueprint, request, jsonify
from db import get_db_connection

eleccion_bp = Blueprint('eleccion', __name__)

# -------------------- Elección --------------------
@eleccion_bp.route('/elecciones', methods=['GET'])
def listar_elecciones():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM eleccion")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@eleccion_bp.route('/eleccion', methods=['POST'])
def crear_eleccion():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO eleccion (fecha, id_tipo_eleccion) VALUES (%s, %s)",
                   (data['fecha'], data['id_tipo_eleccion']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Elección creada'})

@eleccion_bp.route('/eleccion/<int:id>', methods=['PUT'])
def modificar_eleccion(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE eleccion SET fecha = %s, id_tipo_eleccion = %s WHERE id = %s",
                   (data['fecha'], data['id_tipo_eleccion'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Elección modificada'})

@eleccion_bp.route('/eleccion/<int:id>', methods=['DELETE'])
def eliminar_eleccion(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM eleccion WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Elección eliminada'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar elección: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()