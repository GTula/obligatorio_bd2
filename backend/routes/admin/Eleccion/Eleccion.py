
from flask import Blueprint, request, jsonify
from db import get_db_connection

eleccion_bp = Blueprint('eleccion', __name__)

# -------------------- Elección --------------------
@eleccion_bp.route('/elecciones', methods=['GET'])
def listar_elecciones():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM eleccion")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@eleccion_bp.route('/eleccion', methods=['POST'])
def crear_eleccion():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO eleccion (fecha, id_tipo_eleccion) VALUES (%s, %s)",
                   (data['fecha'], data['id_tipo_eleccion']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Elección creada'})

@eleccion_bp.route('/eleccion/<int:id>', methods=['PUT'])
def modificar_eleccion(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE eleccion SET fecha = %s, id_tipo_eleccion = %s WHERE id = %s",
                   (data['fecha'], data['id_tipo_eleccion'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Elección modificada'})

@eleccion_bp.route('/eleccion/<int:id>', methods=['DELETE'])
def eliminar_eleccion(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM eleccion WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Elección eliminada'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar elección: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@eleccion_bp.route('/eleccion/verificar-eliminacion/<int:id>', methods=['GET'])
def verificar_eliminacion_eleccion(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) as total FROM voto WHERE id_eleccion = %s", (id,))
        votos = cursor.fetchone()['total']
        
        return jsonify({
            'puede_eliminar': votos == 0,
            'votos_registrados': votos,
            'mensaje': 'No se puede eliminar una elección con votos registrados' if votos > 0 else 'Se puede eliminar'
        })
    finally:
        cursor.close()
        conn.close()

@eleccion_bp.route('/eleccion/forzar/<int:id>', methods=['DELETE'])
def forzar_eliminar_eleccion(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Verificar votos primero
        cursor.execute("SELECT COUNT(*) as total FROM voto WHERE id_eleccion = %s", (id,))
        if cursor.fetchone()[0] > 0:
            return jsonify({'error': 'No se puede eliminar una elección con votos registrados. Use el panel de administración para limpiar votos primero.'}), 400
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        eliminaciones = [
            "DELETE FROM vota_en WHERE id_eleccion = %s",
            "DELETE FROM asignado WHERE id_eleccion = %s",
            "DELETE FROM participacion_en_mesa WHERE id_eleccion = %s",
            "DELETE FROM mesa WHERE id_eleccion = %s",
            "DELETE FROM candidato_por_lista WHERE id_eleccion = %s",
            "DELETE FROM voto_elige_papeleta WHERE id_eleccion = %s",
            "DELETE FROM lista WHERE id_eleccion = %s",
            "DELETE FROM papeleta_plebiscito WHERE id_eleccion = %s",
            "DELETE FROM papeleta WHERE id_eleccion = %s",
            "DELETE FROM circuito WHERE id_eleccion = %s",
            "DELETE FROM eleccion WHERE id = %s"
        ]
        
        for sql in eliminaciones:
            cursor.execute(sql, (id,))
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Elección eliminada forzadamente (sin votos)'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
