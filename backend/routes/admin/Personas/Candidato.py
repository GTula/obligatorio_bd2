
from flask import Blueprint, request, jsonify
from db import get_db_connection

candidato_bp = Blueprint('candidato', __name__)

# -------------------- Candidato (continuación) --------------------
@candidato_bp.route('/candidatos', methods=['GET'])
def listar_autoridades():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM candidato")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@candidato_bp.route('/candidato', methods=['POST'])
def crear_candidato():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        ci_ciudadano = data.get('ci_ciudadano')
        if not ci_ciudadano:
            return jsonify({'error': 'ci_ciudadano es requerido'}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar que el ciudadano existe
        cursor.execute("SELECT ci FROM ciudadano WHERE ci = %s", (ci_ciudadano,))
        if not cursor.fetchone():
            return jsonify({'error': 'El ciudadano no existe'}), 400
            
        # Verificar que no sea ya candidato
        cursor.execute("SELECT ci_ciudadano FROM candidato WHERE ci_ciudadano = %s", (ci_ciudadano,))
        if cursor.fetchone():
            return jsonify({'error': 'El ciudadano ya es candidato'}), 400
            
        # Insertar candidato
        cursor.execute("INSERT INTO candidato (ci_ciudadano) VALUES (%s)", (ci_ciudadano,))
        conn.commit()
        
        return jsonify({'mensaje': 'Candidato creado exitosamente'}), 201
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error creando candidato: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error interno: {str(e)}'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@candidato_bp.route('/candidato/<ci>', methods=['DELETE'])
def eliminar_candidato(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM candidato WHERE ci_ciudadano = %s", (ci,))
        conn.commit()
        return jsonify({'mensaje': 'Candidato eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar candidato: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()