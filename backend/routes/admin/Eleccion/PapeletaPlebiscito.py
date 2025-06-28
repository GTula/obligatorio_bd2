from flask import Blueprint, request, jsonify
from db import get_db_connection
import traceback

papeleta_plebiscito_bp = Blueprint('papeleta_plebiscito', __name__)

@papeleta_plebiscito_bp.route('', methods=['POST'])
def crear_papeleta_plebiscito():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Validar que la elección sea tipo plebiscito (3)
        cursor.execute("SELECT tipo FROM eleccion WHERE id = %s", (data['id_eleccion'],))
        eleccion = cursor.fetchone()
        
        if not eleccion:
            return jsonify({'error': 'Elección no encontrada'}), 404
        
        if eleccion[0] != 3:  # Tipo plebiscito
            return jsonify({'error': 'La papeleta plebiscito solo puede pertenecer a elecciones tipo plebiscito'}), 400
        
        # 2. Validar que no exista una lista con el mismo id_papeleta e id_eleccion
        cursor.execute("SELECT * FROM lista WHERE id_papeleta = %s AND id_eleccion = %s", 
                      (data['id_papeleta'], data['id_eleccion']))
        if cursor.fetchone():
            return jsonify({'error': 'Ya existe una lista con este id_papeleta e id_eleccion. No puede pertenecer a ambos'}), 400
        
        # 3. Verificar si ya existe la papeleta base, si no, crearla
        cursor.execute("SELECT * FROM papeleta WHERE id = %s AND id_eleccion = %s", 
                      (data['id_papeleta'], data['id_eleccion']))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO papeleta (id, id_eleccion) VALUES (%s, %s)",
                          (data['id_papeleta'], data['id_eleccion']))
        
        # 4. Insertar en papeleta_plebiscito
        cursor.execute("INSERT INTO papeleta_plebiscito (id_papeleta, id_eleccion, nombre, valor) VALUES (%s, %s, %s, %s)",
                       (data['id_papeleta'], data['id_eleccion'], data['nombre'], data['valor']))
        
        conn.commit()
        return jsonify({'mensaje': 'Papeleta plebiscito creada'}), 201
        
    except Exception as e:
        conn.rollback()
        print(f"Error creating papeleta_plebiscito: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@papeleta_plebiscito_bp.route('/<int:id_papeleta>/<int:id_eleccion>', methods=['PUT'])
def modificar_papeleta_plebiscito(id_papeleta, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Validar que existe
        cursor.execute("SELECT * FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s",
                      (id_papeleta, id_eleccion))
        if not cursor.fetchone():
            return jsonify({'error': 'Papeleta plebiscito no encontrada'}), 404
        
        cursor.execute("UPDATE papeleta_plebiscito SET nombre = %s, valor = %s WHERE id_papeleta = %s AND id_eleccion = %s",
                       (data['nombre'], data['valor'], id_papeleta, id_eleccion))
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'No se pudo actualizar la papeleta plebiscito'}), 400
        
        conn.commit()
        return jsonify({'mensaje': 'Papeleta plebiscito modificada'})
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating papeleta_plebiscito: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@papeleta_plebiscito_bp.route('/<int:id_papeleta>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_papeleta_plebiscito(id_papeleta, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar que existe
        cursor.execute("SELECT * FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s",
                      (id_papeleta, id_eleccion))
        if not cursor.fetchone():
            return jsonify({'error': 'Papeleta plebiscito no encontrada'}), 404
        
        # Eliminar papeleta_plebiscito
        cursor.execute("DELETE FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s",
                       (id_papeleta, id_eleccion))
        
        # Opcional: Eliminar papeleta base si no tiene otras referencias
        cursor.execute("SELECT COUNT(*) FROM lista WHERE id_papeleta = %s AND id_eleccion = %s", 
                      (id_papeleta, id_eleccion))
        lista_count = cursor.fetchone()[0]
        
        if lista_count == 0:
            cursor.execute("DELETE FROM papeleta WHERE id = %s AND id_eleccion = %s", 
                          (id_papeleta, id_eleccion))
        
        conn.commit()
        return jsonify({'mensaje': 'Papeleta plebiscito eliminada'})
        
    except Exception as e:
        conn.rollback()
        print(f"Error deleting papeleta_plebiscito: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Endpoint para listar papeletas plebiscito
@papeleta_plebiscito_bp.route('/papeletas-plebiscito', methods=['GET'])
def listar_papeletas_plebiscito():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT pp.*, e.tipo as tipo_eleccion 
            FROM papeleta_plebiscito pp 
            JOIN eleccion e ON pp.id_eleccion = e.id
        """)
        data = cursor.fetchall()
        return jsonify(data)
        
    except Exception as e:
        print(f"Error listing papeletas_plebiscito: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
