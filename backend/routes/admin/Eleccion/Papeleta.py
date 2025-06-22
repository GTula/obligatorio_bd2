
from flask import Blueprint, request, jsonify
from db import get_db_connection

papeleta_bp = Blueprint('papeleta', __name__)

# -------------------- Papeleta --------------------
@papeleta_bp.route('/papeletas', methods=['GET'])
def listar_papeletas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM papeleta")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@papeleta_bp.route('', methods=['POST'])
def crear_papeleta():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO papeleta (id_eleccion) VALUES (%s)",
                   (data['id_eleccion'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Papeleta creada'})

@papeleta_bp.route('/<int:id>/<int:id_eleccion>', methods=['PUT'])
def modificar_papeleta(id, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE papeleta SET id_eleccion = %s WHERE id = %s AND id_eleccion = %s",
                   (data['id_eleccion'], id, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Papeleta modificada'})

@papeleta_bp.route('/<int:id>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_papeleta(id, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM papeleta WHERE id = %s AND id_eleccion = %s", (id, id_eleccion))
        conn.commit()
        return jsonify({'mensaje': 'Papeleta eliminada'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar papeleta: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()