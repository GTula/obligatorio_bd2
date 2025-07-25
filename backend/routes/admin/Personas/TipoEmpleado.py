
from flask import Blueprint, request, jsonify
from db import get_db_connection

tipo_empleado_bp = Blueprint('tipo-empleado', __name__)


# -------------------- Tipo Empleado --------------------
@tipo_empleado_bp.route('/tipos-empleado', methods=['GET'])
def listar_tipos_empleado():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tipo_empleado")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@tipo_empleado_bp.route('/tipo-empleado', methods=['POST'])
def crear_tipo_empleado():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tipo_empleado (nombre) VALUES (%s)", (data['nombre'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Tipo de empleado creado'})

@tipo_empleado_bp.route('/tipo-empleado/<int:id>', methods=['PUT'])
def modificar_tipo_empleado(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tipo_empleado SET nombre = %s WHERE id = %s", (data['nombre'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Tipo de empleado modificado'})

@tipo_empleado_bp.route('/tipo-empleado/<int:id>', methods=['DELETE'])
def eliminar_tipo_empleado(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tipo_empleado WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Tipo de empleado eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar tipo de empleado: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@tipo_empleado_bp.route('/tipo-empleado/forzar/<int:id>', methods=['DELETE'])
def forzar_eliminar_tipo_empleado(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM participacion_en_mesa WHERE id_tipo = %s", (id,))
        cursor.execute("DELETE FROM tipo_empleado WHERE id = %s", (id,))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Tipo de empleado eliminado forzadamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
