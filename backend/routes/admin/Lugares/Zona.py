
from flask import Blueprint, request, jsonify
from db import get_db_connection

zona_bp = Blueprint('zona', __name__)


# -------------------- Zona --------------------
@zona_bp.route('/zonas', methods=['GET'])
def listar_zonas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM zona")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@zona_bp.route('', methods=['POST'])
def crear_zona():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO zona (nombre, id_departamento) VALUES (%s, %s)",
                   (data['nombre'], data['id_departamento']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Zona creada'})

@zona_bp.route('/<int:id>/<int:id_departamento>', methods=['PUT'])
def modificar_zona(id, id_departamento):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE zona SET nombre = %s WHERE id = %s AND id_departamento = %s",
                   (data['nombre'], id, id_departamento))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Zona modificada'})

@zona_bp.route('/<int:id>/<int:id_departamento>', methods=['DELETE'])
def eliminar_zona(id, id_departamento):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM establecimiento WHERE id_zona = %s AND id_departamento = %s", (id, id_departamento))
        if cursor.fetchone():
            return jsonify({'error': 'No se puede eliminar zona con establecimientos asociados'}), 400
        cursor.execute("DELETE FROM zona WHERE id = %s AND id_departamento = %s", (id, id_departamento))
        conn.commit()
        return jsonify({'mensaje': 'Zona eliminada'})
    finally:
        cursor.close()
        conn.close()
