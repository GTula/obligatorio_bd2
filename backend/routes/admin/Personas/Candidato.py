
from flask import Blueprint, request, jsonify
from db import get_db_connection

candidato_bp = Blueprint('candidato', __name__)

# -------------------- Candidato (continuación) --------------------
@candidato_bp.route('/candidato', methods=['POST'])
def crear_candidato():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO candidato (ci_ciudadano, id_partido) VALUES (%s, %s)",
                   (data['ci_ciudadano'], data['id_partido']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Candidato creado'})

@candidato_bp.route('/<ci>', methods=['PUT'])
def modificar_candidato(ci):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE candidato SET id_partido = %s WHERE ci_ciudadano = %s",
                   (data['id_partido'], ci))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Candidato modificado'})

@candidato_bp.route('/<ci>', methods=['DELETE'])
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
