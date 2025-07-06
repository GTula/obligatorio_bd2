        
from flask import Blueprint, request, jsonify
from db import get_db_connection
import traceback

lista_bp = Blueprint('lista', __name__)

@lista_bp.route('/listas', methods=['GET'])
def listar_listas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lista")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@lista_bp.route('/lista', methods=['POST'])
def crear_lista():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar que la papeleta no esté ya en papeleta_plebiscito
        cursor.execute("SELECT id_papeleta FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s",
                       (data['id_papeleta'], data['id_eleccion']))
        if cursor.fetchone():
            return jsonify({'error': 'Esta papeleta ya está siendo usada como papeleta de plebiscito'}), 400
        
        # Verificar que la papeleta no esté ya en lista
        cursor.execute("SELECT id_papeleta FROM lista WHERE id_papeleta = %s AND id_eleccion = %s",
                       (data['id_papeleta'], data['id_eleccion']))
        if cursor.fetchone():
            return jsonify({'error': 'Esta papeleta ya está siendo usada como lista'}), 400
        
        # Insertar papeleta
        cursor.execute("INSERT INTO papeleta (id, id_eleccion) VALUES (%s, %s)",
                       (data['id_papeleta'], data['id_eleccion']))
        
        # Insertar lista
        cursor.execute("INSERT INTO lista (id_papeleta, id_eleccion, id_partido, organo, id_departamento) VALUES (%s, %s, %s, %s, %s)",
                       (data['id_papeleta'], data['id_eleccion'], data['id_partido'], data['organo'], data['id_departamento']))
        
        conn.commit()
        return jsonify({'mensaje': 'Lista creada'})
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error creando lista: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()


@lista_bp.route('/lista/<int:id_papeleta>/<int:id_eleccion>', methods=['PUT'])
def modificar_lista(id_papeleta, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE lista SET id_partido = %s, organo = %s, id_departamento = %s WHERE id_papeleta = %s AND id_eleccion = %s",
                   (data['id_partido'], data['organo'], data['id_departamento'], id_papeleta, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Lista modificada'})

@lista_bp.route('/lista/<int:id_papeleta>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_lista(id_papeleta, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM lista WHERE id_papeleta = %s AND id_eleccion = %s", (id_papeleta, id_eleccion))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM papeleta WHERE id = %s AND id_eleccion = %s",
                   (id_papeleta, id_eleccion))
        conn.commit()
        return jsonify({'mensaje': 'Lista eliminada'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar lista: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()
