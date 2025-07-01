
from flask import Blueprint, request, jsonify
from db import get_db_connection

ciudadano_bp = Blueprint('ciudadano', __name__)

# -------------------- Ciudadano --------------------
@ciudadano_bp.route('/ciudadanos', methods=['GET'])
def listar_ciudadanos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ciudadano")
    ciudadanos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(ciudadanos)

@ciudadano_bp.route('/ciudadano', methods=['POST'])
def crear_ciudadano():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ciudadano (ci, nombre, apellido, fecha_nac) VALUES (%s, %s, %s, %s)",
                   (data['ci'], data['nombre'], data['apellido'], data['fecha_nac']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Ciudadano creado'}), 201

@ciudadano_bp.route('/ciudadano/<ci>', methods=['PUT'])
def editar_ciudadano(ci):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE ciudadano SET nombre = %s, apellido = %s, fecha_nac = %s WHERE ci = %s",
                       (data['nombre'], data['apellido'], data['fecha_nac'], ci))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Ciudadano actualizado'})
    except Exception as e:
        return jsonify({'error': f'Error updating ciudadano: {str(e)}'}), 500

@ciudadano_bp.route('/ciudadano/<ci>', methods=['DELETE'])
def eliminar_ciudadano(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ciudadano WHERE ci = %s", (ci,))
        conn.commit()
        return jsonify({'mensaje': 'Ciudadano eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar ciudadano: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@ciudadano_bp.route('/ciudadano/forzar/<ci>', methods=['DELETE'])
def forzar_eliminar_ciudadano(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM ciudadano WHERE ci = %s", (ci,))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Ciudadano eliminado forzadamente'})
    finally:
        cursor.close()
        conn.close()