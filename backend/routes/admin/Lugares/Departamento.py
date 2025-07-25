
from flask import Blueprint, request, jsonify
from db import get_db_connection

departamento_bp = Blueprint('departamento', __name__)


# -------------------- Departamento --------------------
@departamento_bp.route('/departamentos', methods=['GET'])
def listar_departamentos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM departamento")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@departamento_bp.route('/departamento', methods=['POST'])
def crear_departamento():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO departamento (nombre) VALUES (%s)", (data['nombre'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Departamento creado'})

@departamento_bp.route('/departamento/<int:id>', methods=['PUT'])
def modificar_departamento(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE departamento SET nombre = %s WHERE id = %s", (data['nombre'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Departamento modificado'})

@departamento_bp.route('/departamento/<int:id>', methods=['DELETE'])
def eliminar_departamento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM zona WHERE id_departamento = %s", (id,))
        if cursor.fetchone():
            return jsonify({'error': 'No se puede eliminar un departamento con zonas asociadas'}), 400
        cursor.execute("DELETE FROM departamento WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Departamento eliminado'})
    finally:
        cursor.close()
        conn.close()

@departamento_bp.route('/departamento/forzar/<int:id>', methods=['DELETE'])
def forzar_eliminar_departamento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        eliminaciones = [
            "DELETE FROM lista WHERE id_departamento = %s",
            "DELETE FROM establecimiento WHERE id_departamento = %s",
            "DELETE FROM zona WHERE id_departamento = %s",
            "DELETE FROM departamento WHERE id = %s"
        ]
        
        for sql in eliminaciones:
            cursor.execute(sql, (id,))
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Departamento eliminado forzadamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
