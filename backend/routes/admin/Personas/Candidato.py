
from flask import Blueprint, request, jsonify
from db import get_db_connection

candidato_bp = Blueprint('candidato', __name__)

# -------------------- Candidato (continuación) --------------------
@candidato_bp.route('/candidato', methods=['POST'])
def crear_candidato():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO candidato (ci_ciudadano) VALUES (%s)",
                   (data['ci_ciudadano']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Candidato creado'})



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