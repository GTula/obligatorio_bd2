from flask import Blueprint, request, jsonify
from db import get_db_connection
import traceback

papeleta_plebiscito_bp = Blueprint('papeleta-plebiscito', __name__)

@papeleta_plebiscito_bp.route('/papeleta-plebiscito', methods=['POST'])
def crear_papeleta_plebiscito():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar que la papeleta no esté ya en lista
        cursor.execute("SELECT id_papeleta FROM lista WHERE id_papeleta = %s AND id_eleccion = %s",
                       (data['id_papeleta'], data['id_eleccion']))
        if cursor.fetchone():
            return jsonify({'error': 'Esta papeleta ya está siendo usada como lista'}), 400
        
        # Verificar que la papeleta no esté ya en papeleta_plebiscito
        cursor.execute("SELECT id_papeleta FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s",
                       (data['id_papeleta'], data['id_eleccion']))
        if cursor.fetchone():
            return jsonify({'error': 'Esta papeleta ya está siendo usada como papeleta de plebiscito'}), 400
        
        # Insertar papeleta
        cursor.execute("INSERT INTO papeleta (id, id_eleccion) VALUES (%s, %s)",
                       (data['id_papeleta'], data['id_eleccion']))
        
        # Insertar papeleta_plebiscito
        cursor.execute("INSERT INTO papeleta_plebiscito (id_papeleta, id_eleccion, nombre, valor) VALUES (%s, %s, %s, %s)",
                       (data['id_papeleta'], data['id_eleccion'], data['nombre'], data['valor']))
        
        conn.commit()
        return jsonify({'mensaje': 'Papeleta plebiscito creada'})
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error creando papeleta plebiscito: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()

@papeleta_plebiscito_bp.route('/papeleta-plebiscito/<int:id_papeleta>/<int:id_eleccion>', methods=['PUT'])
def modificar_papeleta_plebiscito(id_papeleta, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE papeleta_plebiscito SET nombre = %s, valor = %s WHERE id_papeleta = %s AND id_eleccion = %s",
                   (data['nombre'], data['valor'], id_papeleta, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Papeleta plebiscito modificada'})

@papeleta_plebiscito_bp.route('/papeleta-plebiscito/<int:id_papeleta>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_papeleta_plebiscito(id_papeleta, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s",
                   (id_papeleta, id_eleccion))
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM papeleta WHERE id = %s AND id_eleccion = %s",
                   (id_papeleta, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Papeleta plebiscito eliminada'})

@papeleta_plebiscito_bp.route('/papeletas-plebiscito', methods=['GET'])
def listar_papeletas_plebiscito():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT pp.id_papeleta, pp.id_eleccion, pp.nombre, pp.valor, e.fecha as fecha_eleccion
        FROM papeleta_plebiscito pp
        JOIN eleccion e ON pp.id_eleccion = e.id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@papeleta_plebiscito_bp.route('/papeleta-plebiscito/forzar/<int:id_papeleta>/<int:id_eleccion>', methods=['DELETE'])
def forzar_eliminar_papeleta_plebiscito(id_papeleta, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM voto_elige_papeleta WHERE id_papeleta = %s AND id_eleccion = %s", (id_papeleta, id_eleccion))
        cursor.execute("DELETE FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s", (id_papeleta, id_eleccion))
        cursor.execute("DELETE FROM papeleta WHERE id = %s AND id_eleccion = %s", (id_papeleta, id_eleccion))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Papeleta plebiscito eliminada forzadamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
