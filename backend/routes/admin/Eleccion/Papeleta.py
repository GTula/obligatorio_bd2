from flask import Blueprint, request, jsonify
from db import get_db_connection
import traceback

papeleta_bp = Blueprint('papeleta', __name__)

@papeleta_bp.route('/papeletas', methods=['GET'])
def listar_papeletas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT p.*, e.tipo as tipo_eleccion, e.fecha,
                   CASE 
                       WHEN pp.id_papeleta IS NOT NULL THEN 'plebiscito'
                       WHEN l.id_papeleta IS NOT NULL THEN 'lista'
                       ELSE 'base'
                   END as tipo_papeleta
            FROM papeleta p
            JOIN eleccion e ON p.id_eleccion = e.id
            LEFT JOIN papeleta_plebiscito pp ON p.id = pp.id_papeleta AND p.id_eleccion = pp.id_eleccion
            LEFT JOIN lista l ON p.id = l.id_papeleta AND p.id_eleccion = l.id_eleccion
        """)
        data = cursor.fetchall()
        return jsonify(data)
        
    except Exception as e:
        print(f"Error listing papeletas: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@papeleta_bp.route('', methods=['POST'])
def crear_papeleta():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Validar que la elección existe
        cursor.execute("SELECT * FROM eleccion WHERE id = %s", (data['id_eleccion'],))
        if not cursor.fetchone():
            return jsonify({'error': 'Elección no encontrada'}), 404
        
        # Verificar que no existe ya
        cursor.execute("SELECT * FROM papeleta WHERE id = %s AND id_eleccion = %s", 
                      (data.get('id'), data['id_eleccion']))
        if cursor.fetchone():
            return jsonify({'error': 'Ya existe una papeleta con este ID para esta elección'}), 409
        
        # Insertar papeleta base
        if 'id' in data:
            cursor.execute("INSERT INTO papeleta (id, id_eleccion) VALUES (%s, %s)",
                          (data['id'], data['id_eleccion']))
        else:
            cursor.execute("INSERT INTO papeleta (id_eleccion) VALUES (%s)",
                          (data['id_eleccion'],))
        
        conn.commit()
        return jsonify({'mensaje': 'Papeleta creada'}), 201
        
    except Exception as e:
        conn.rollback()
        print(f"Error creating papeleta: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@papeleta_bp.route('/<int:id>/<int:id_eleccion>', methods=['PUT'])
def modificar_papeleta(id, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar que existe
        cursor.execute("SELECT * FROM papeleta WHERE id = %s AND id_eleccion = %s", (id, id_eleccion))
        if not cursor.fetchone():
            return jsonify({'error': 'Papeleta no encontrada'}), 404
        
        # Validar nueva elección si se está cambiando
        if 'id_eleccion' in data and data['id_eleccion'] != id_eleccion:
            cursor.execute("SELECT * FROM eleccion WHERE id = %s", (data['id_eleccion'],))
            if not cursor.fetchone():
                return jsonify({'error': 'Nueva elección no encontrada'}), 404
        
        cursor.execute("UPDATE papeleta SET id_eleccion = %s WHERE id = %s AND id_eleccion = %s",
                       (data['id_eleccion'], id, id_eleccion))
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'No se pudo actualizar la papeleta'}), 400
        
        conn.commit()
        return jsonify({'mensaje': 'Papeleta modificada'})
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating papeleta: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@papeleta_bp.route('/<int:id>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_papeleta(id, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar que existe
        cursor.execute("SELECT * FROM papeleta WHERE id = %s AND id_eleccion = %s", (id, id_eleccion))
        if not cursor.fetchone():
            return jsonify({'error': 'Papeleta no encontrada'}), 404
        
        # Verificar que no tiene papeletas_plebiscito asociadas
        cursor.execute("SELECT * FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s", 
                      (id, id_eleccion))
        if cursor.fetchone():
            return jsonify({'error': 'No se puede eliminar papeleta con papeletas plebiscito asociadas'}), 400
        
        # Verificar que no tiene listas asociadas
        cursor.execute("SELECT * FROM lista WHERE id_papeleta = %s AND id_eleccion = %s", 
                      (id, id_eleccion))
        if cursor.fetchone():
            return jsonify({'error': 'No se puede eliminar papeleta con listas asociadas'}), 400
        
        cursor.execute("DELETE FROM papeleta WHERE id = %s AND id_eleccion = %s", (id, id_eleccion))
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'No se pudo eliminar la papeleta'}), 400
        
        conn.commit()
        return jsonify({'mensaje': 'Papeleta eliminada'})
        
    except Exception as e:
        conn.rollback()
        print(f"Error deleting papeleta: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Endpoint para obtener papeletas disponibles para una elección
@papeleta_bp.route('/disponibles/<int:id_eleccion>', methods=['GET'])
def papeletas_disponibles(id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT p.*, 
                   CASE 
                       WHEN pp.id_papeleta IS NOT NULL THEN 'ocupada_plebiscito'
                       WHEN l.id_papeleta IS NOT NULL THEN 'ocupada_lista'
                       ELSE 'disponible'
                   END as estado
            FROM papeleta p
            LEFT JOIN papeleta_plebiscito pp ON p.id = pp.id_papeleta AND p.id_eleccion = pp.id_eleccion
            LEFT JOIN lista l ON p.id = l.id_papeleta AND p.id_eleccion = l.id_eleccion
            WHERE p.id_eleccion = %s
        """, (id_eleccion,))
        
        data = cursor.fetchall()
        return jsonify(data)
        
    except Exception as e:
        print(f"Error getting available papeletas: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
