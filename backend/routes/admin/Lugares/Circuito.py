
from flask import Blueprint, request, jsonify
from db import get_db_connection

circuito_bp = Blueprint('circuito', __name__)


# -------------------- Circuito --------------------
@circuito_bp.route('/circuitos', methods=['GET'])
def listar_circuitos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM circuito")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@circuito_bp.route('/circuito', methods=['POST'])
def crear_circuito():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO circuito (id_eleccion, accesible, id_establecimiento) VALUES (%s, %s, %s)",
                   (data['id_eleccion'], data['accesible'], data['id_establecimiento']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Circuito creado'})

@circuito_bp.route('/circuito/<int:id>/<int:id_eleccion>', methods=['PUT'])
def modificar_circuito(id, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE circuito SET accesible = %s, id_establecimiento = %s WHERE id = %s AND id_eleccion = %s",
                       (data['accesible'], data['id_establecimiento'], id, id_eleccion))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Circuito no encontrado'}), 404
        conn.commit()
        return jsonify({'mensaje': 'Circuito modificado'})
    except Exception as e:
        return jsonify({'error': f'Error modificando circuito: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()

@circuito_bp.route('/circuito/<int:id>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_circuito(id, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM circuito WHERE id = %s AND id_eleccion = %s", (id, id_eleccion))
        conn.commit()
        return jsonify({'mensaje': 'Circuito eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar circuito: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@circuito_bp.route('/circuito/forzar/<int:id>/<int:id_eleccion>', methods=['DELETE'])
def forzar_eliminar_circuito(id, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        eliminaciones = [
            "DELETE FROM voto WHERE id_circuito = %s AND id_eleccion = %s",
            "DELETE FROM vota_en WHERE id_circuito = %s AND id_eleccion = %s",
            "DELETE FROM asignado WHERE id_circuito = %s AND id_eleccion = %s",
            "DELETE FROM participacion_en_mesa WHERE id_circuito = %s AND id_eleccion = %s",
            "DELETE FROM mesa WHERE id_circuito = %s AND id_eleccion = %s",
            "DELETE FROM circuito WHERE id = %s AND id_eleccion = %s"
        ]
        
        for sql in eliminaciones:
            cursor.execute(sql, (id, id_eleccion))
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Circuito eliminado forzadamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
