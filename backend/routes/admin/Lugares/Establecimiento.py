
from flask import Blueprint, request, jsonify
from db import get_db_connection

establecimiento_bp = Blueprint('establecimiento', __name__)

# -------------------- Establecimiento --------------------
@establecimiento_bp.route('/establecimientos', methods=['GET'])
def listar_establecimientos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM establecimiento")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@establecimiento_bp.route('', methods=['POST'])
def crear_establecimiento():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO establecimiento (direccion, id_zona, id_departamento) VALUES (%s, %s, %s)",
                   (data['direccion'], data['id_zona'], data['id_departamento']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Establecimiento creado'})

@establecimiento_bp.route('/<int:id>', methods=['PUT'])
def modificar_establecimiento(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE establecimiento SET direccion = %s, id_zona = %s, id_departamento = %s WHERE id = %s",
                   (data['direccion'], data['id_zona'], data['id_departamento'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Establecimiento modificado'})

@establecimiento_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_establecimiento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM circuito WHERE id_establecimiento = %s", (id,))
        if cursor.fetchone():
            return jsonify({'error': 'No se puede eliminar establecimiento asociado a circuito'}), 400
        cursor.execute("DELETE FROM establecimiento WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Establecimiento eliminado'})
    finally:
        cursor.close()
        conn.close()