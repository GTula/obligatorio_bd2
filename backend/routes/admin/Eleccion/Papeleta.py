from flask import Blueprint, request, jsonify
from db import get_db_connection
import traceback

papeleta_bp = Blueprint('papeleta', __name__)

@papeleta_bp.route('/papeletas', methods=['GET'])
def listar_papeletas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM papeleta")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@papeleta_bp.route('/papeleta', methods=['POST'])
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

@papeleta_bp.route('/papeleta/<int:id>/<int:id_eleccion>', methods=['PUT'])
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

@papeleta_bp.route('/papeleta/<int:id>/<int:id_eleccion>', methods=['DELETE'])
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

@papeleta_bp.route('/papeleta/forzar/<int:id>/<int:id_eleccion>', methods=['DELETE'])
def forzar_eliminar_papeleta(id, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        eliminaciones = [
            "DELETE FROM voto_elige_papeleta WHERE id_papeleta = %s AND id_eleccion = %s",
            "DELETE FROM candidato_por_lista WHERE id_papeleta = %s AND id_eleccion = %s",
            "DELETE FROM lista WHERE id_papeleta = %s AND id_eleccion = %s",
            "DELETE FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s",
            "DELETE FROM papeleta WHERE id = %s AND id_eleccion = %s"
        ]
        
        for sql in eliminaciones:
            cursor.execute(sql, (id, id_eleccion))
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Papeleta eliminada forzadamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
