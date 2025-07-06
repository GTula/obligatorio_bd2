
from flask import Blueprint, request, jsonify
from db import get_db_connection

establecimiento_bp = Blueprint('establecimiento', __name__)

# -------------------- Establecimiento --------------------
@establecimiento_bp.route('/establecimientos', methods=['GET'])
def listar_establecimientos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.id, e.direccion, e.id_zona, e.id_departamento, 
               z.nombre as zona_nombre, d.nombre as departamento_nombre
        FROM establecimiento e
        JOIN zona z ON e.id_zona = z.id AND e.id_departamento = z.id_departamento
        JOIN departamento d ON e.id_departamento = d.id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@establecimiento_bp.route('/establecimiento', methods=['POST'])
def crear_establecimiento():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Verificar que zona y departamento coinciden
        cursor.execute("SELECT id FROM zona WHERE id = %s AND id_departamento = %s", 
                       (data['id_zona'], data['id_departamento']))
        if not cursor.fetchone():
            return jsonify({'error': 'La zona no pertenece al departamento seleccionado'}), 400
            
        cursor.execute("INSERT INTO establecimiento (direccion, id_zona, id_departamento) VALUES (%s, %s, %s)",
                       (data['direccion'], data['id_zona'], data['id_departamento']))
        conn.commit()
        return jsonify({'mensaje': 'Establecimiento creado'})
    except Exception as e:
        return jsonify({'error': f'Error creando establecimiento: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()

@establecimiento_bp.route('/establecimiento/<int:id>', methods=['PUT'])
def modificar_establecimiento(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Verificar que zona y departamento coinciden
        cursor.execute("SELECT id FROM zona WHERE id = %s AND id_departamento = %s", 
                       (data['id_zona'], data['id_departamento']))
        if not cursor.fetchone():
            return jsonify({'error': 'La zona no pertenece al departamento seleccionado'}), 400
            
        cursor.execute("UPDATE establecimiento SET direccion = %s, id_zona = %s, id_departamento = %s WHERE id = %s",
                       (data['direccion'], data['id_zona'], data['id_departamento'], id))
        conn.commit()
        return jsonify({'mensaje': 'Establecimiento modificado'})
    except Exception as e:
        return jsonify({'error': f'Error modificando establecimiento: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()

@establecimiento_bp.route('/establecimiento/<int:id>', methods=['DELETE'])
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

@establecimiento_bp.route('/establecimiento/forzar/<int:id>', methods=['DELETE'])
def forzar_eliminar_establecimiento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM agente_establecimiento WHERE id_establecimiento = %s", (id,))
        cursor.execute("DELETE FROM circuito WHERE id_establecimiento = %s", (id,))
        cursor.execute("DELETE FROM establecimiento WHERE id = %s", (id,))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Establecimiento eliminado forzadamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
