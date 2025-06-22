
from flask import Blueprint, request, jsonify
from db import get_db_connection

tipo_eleccion_bp = Blueprint('tipo_eleccion', __name__)

# -------------------- Tipo Elección --------------------
@tipo_eleccion_bp.route('/tipos-eleccion', methods=['GET'])
def listar_tipos_eleccion():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tipo_eleccion")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@tipo_eleccion_bp.route('', methods=['POST'])
def crear_tipo_eleccion():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tipo_eleccion (nombre) VALUES (%s)", (data['nombre'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Tipo de elección creado'})

@tipo_eleccion_bp.route('/<int:id>', methods=['PUT'])
def modificar_tipo_eleccion(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tipo_eleccion SET nombre = %s WHERE id = %s", (data['nombre'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Tipo de elección modificado'})

@tipo_eleccion_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_tipo_eleccion(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tipo_eleccion WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Tipo de elección eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar tipo de elección: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()
