
from flask import Blueprint, request, jsonify
from db import get_db_connection

comisaria_bp = Blueprint('comisaria', __name__)

# -------------------- Comisaria --------------------
@comisaria_bp.route('/comisarias', methods=['GET'])
def listar_comisarias():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM comisaria")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@comisaria_bp.route('/comisaria', methods=['POST'])
def crear_comisaria():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comisaria (nombre) VALUES (%s)", (data['nombre'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Comisaría creada'})

@comisaria_bp.route('/comisaria/<int:id>', methods=['PUT'])
def modificar_comisaria(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE comisaria SET nombre = %s WHERE id = %s", (data['nombre'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Comisaría modificada'})

@comisaria_bp.route('/comisaria/<int:id>', methods=['DELETE'])
def eliminar_comisaria(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comisaria WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Comisaría eliminada'})