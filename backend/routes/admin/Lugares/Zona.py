
from flask import Blueprint, request, jsonify
from db import get_db_connection

zona_bp = Blueprint('zona', __name__)


# -------------------- Zona --------------------
@zona_bp.route('/zona/<int:id>/<int:id_departamento>', methods=['PUT'])
def modificar_zona(id, id_departamento):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE zona SET nombre = %s WHERE id = %s AND id_departamento = %s",
                       (data['nombre'], id, id_departamento))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Zona no encontrada'}), 404
        conn.commit()
        return jsonify({'mensaje': 'Zona modificada'})
    except Exception as e:
        return jsonify({'error': f'Error modificando zona: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()

@zona_bp.route('/zonas', methods=['GET'])
def listar_zonas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT z.id, z.nombre, z.id_departamento, d.nombre as departamento_nombre
        FROM zona z
        JOIN departamento d ON z.id_departamento = d.id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@zona_bp.route('/zona', methods=['POST'])
def crear_zona():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO zona (nombre, id_departamento) VALUES (%s, %s)",
                       (data['nombre'], data['id_departamento']))
        conn.commit()
        return jsonify({'mensaje': 'Zona creada'})
    except Exception as e:
        return jsonify({'error': f'Error creando zona: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()

@zona_bp.route('/zona/<int:id>/<int:id_departamento>', methods=['DELETE'])
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