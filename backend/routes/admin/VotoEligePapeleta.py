from flask import Blueprint, request, jsonify
from db import get_db_connection
import traceback

voto_elige_papeleta_bp = Blueprint('', __name__)


# -------------------- Voto Elige Papeleta (continuación) --------------------
@voto_elige_papeleta_bp.route('/voto-elige-papeleta', methods=['GET'])
def listar_voto_elige_papeleta():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM voto_elige_papeleta")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@voto_elige_papeleta_bp.route('/voto-elige-papeleta', methods=['POST'])
def crear_voto_elige_papeleta():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO voto_elige_papeleta (id_voto_normal, id_papeleta, id_eleccion) VALUES (%s, %s, %s)",
                       (data['id_voto_normal'], data['id_papeleta'], data['id_eleccion']))
        conn.commit()
        return jsonify({'mensaje': 'Voto elige papeleta creado'})
    except Exception as e:
        return jsonify({'error': f'Error creando voto elige papeleta: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()



