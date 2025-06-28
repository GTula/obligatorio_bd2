        
from flask import Blueprint, request, jsonify
from db import get_db_connection
import traceback

lista_bp = Blueprint('lista', __name__)

@lista_bp.route('/listas', methods=['GET'])
def listar_listas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT l.*, e.tipo as tipo_eleccion, p.nombre as nombre_partido 
            FROM lista l 
            JOIN eleccion e ON l.id_eleccion = e.id
            LEFT JOIN partido p ON l.id_partido = p.id
        """)
        data = cursor.fetchall()
        return jsonify(data)
        
    except Exception as e:
        print(f"Error listing listas: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@lista_bp.route('', methods=['POST'])
def crear_lista():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Validar que la elección NO sea tipo plebiscito (3)
        cursor.execute("SELECT tipo FROM eleccion WHERE id = %s", (data['id_eleccion'],))
        eleccion = cursor.fetchone()
        
        if not eleccion:
            return jsonify({'error': 'Elección no encontrada'}), 404
        
        if eleccion[0] == 3:  # Tipo plebiscito
            return jsonify({'error': 'Las listas no pueden pertenecer a elecciones tipo plebiscito'}), 400
        
        # 2. Validar que no exista una papeleta_plebiscito con el mismo id_papeleta e id_eleccion
        cursor.execute("SELECT * FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s", 
                      (data['id_papeleta'], data['id_eleccion']))
        if cursor.fetchone():
            return jsonify({'error': 'Ya existe una papeleta plebiscito con este id_papeleta e id_eleccion. No puede pertenecer a ambos'}), 400
        
        # 3. Validar que el partido existe
        cursor.execute("SELECT * FROM partido WHERE id = %s", (data['id_partido'],))
        if not cursor.fetchone():
            return jsonify({'error': 'Partido no encontrado'}), 404
        
        # 4. Validar que el departamento existe
        cursor.execute("SELECT * FROM departamento WHERE id = %s", (data['id_departamento'],))
        if not cursor.fetchone():
            return jsonify({'error': 'Departamento no encontrado'}), 404
        
        # 5. Verificar si ya existe la papeleta base, si no, crearla
        cursor.execute("SELECT * FROM papeleta WHERE id = %s AND id_eleccion = %s", 
                      (data['id_papeleta'], data['id_eleccion']))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO papeleta (id, id_eleccion) VALUES (%s, %s)",
                          (data['id_papeleta'], data['id_eleccion']))
        
        # 6. Insertar en lista
        cursor.execute("INSERT INTO lista (id_papeleta, id_eleccion, id_partido, organo, id_departamento) VALUES (%s, %s, %s, %s, %s)",
                       (data['id_papeleta'], data['id_eleccion'], data['id_partido'], data['organo'], data['id_departamento']))
        
        conn.commit()
        return jsonify({'mensaje': 'Lista creada'}), 201
        
    except Exception as e:
        conn.rollback()
        print(f"Error creating lista: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@lista_bp.route('/<int:id_papeleta>/<int:id_eleccion>', methods=['PUT'])
def modificar_lista(id_papeleta, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Validar que existe
        cursor.execute("SELECT * FROM lista WHERE id_papeleta = %s AND id_eleccion = %s",
                      (id_papeleta, id_eleccion))
        if not cursor.fetchone():
            return jsonify({'error': 'Lista no encontrada'}), 404
        
        # Validar partido si se está actualizando
        if 'id_partido' in data:
            cursor.execute("SELECT * FROM partido WHERE id = %s", (data['id_partido'],))
            if not cursor.fetchone():
                return jsonify({'error': 'Partido no encontrado'}), 404
        
        # Validar departamento si se está actualizando
        if 'id_departamento' in data:
            cursor.execute("SELECT * FROM departamento WHERE id = %s", (data['id_departamento'],))
            if not cursor.fetchone():
                return jsonify({'error': 'Departamento no encontrado'}), 404
        
        cursor.execute("UPDATE lista SET id_partido = %s, organo = %s, id_departamento = %s WHERE id_papeleta = %s AND id_eleccion = %s",
                       (data['id_partido'], data['organo'], data['id_departamento'], id_papeleta, id_eleccion))
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'No se pudo actualizar la lista'}), 400
        
        conn.commit()
        return jsonify({'mensaje': 'Lista modificada'})
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating lista: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@lista_bp.route('/<int:id_papeleta>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_lista(id_papeleta, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar que existe
        cursor.execute("SELECT * FROM lista WHERE id_papeleta = %s AND id_eleccion = %s",
                      (id_papeleta, id_eleccion))
        if not cursor.fetchone():
            return jsonify({'error': 'Lista no encontrada'}), 404
        
        # Eliminar lista
        cursor.execute("DELETE FROM lista WHERE id_papeleta = %s AND id_eleccion = %s", 
                      (id_papeleta, id_eleccion))
        
        # Opcional: Eliminar papeleta base si no tiene otras referencias
        cursor.execute("SELECT COUNT(*) FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s", 
                      (id_papeleta, id_eleccion))
        plebiscito_count = cursor.fetchone()[0]
        
        if plebiscito_count == 0:
            cursor.execute("DELETE FROM papeleta WHERE id = %s AND id_eleccion = %s", 
                          (id_papeleta, id_eleccion))

        conn.commit()
        return jsonify({'mensaje': 'Lista eliminada'})
        
    except Exception as e:
        conn.rollback()
        print(f"Error deleting lista: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
