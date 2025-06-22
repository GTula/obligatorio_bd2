
from flask import Blueprint, request, jsonify
from db import get_db_connection

credencial_bp = Blueprint('credencial', __name__)


# -------------------- Credencial --------------------
@credencial_bp.route('/credenciales', methods=['GET'])
def listar_credenciales():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM credencial")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@credencial_bp.route('', methods=['POST'])
def crear_credencial():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO credencial (serie, numero, ci_ciudadano) VALUES (%s, %s, %s)",
                   (data['serie'], data['numero'], data['ci_ciudadano']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Credencial creada'})

@credencial_bp.route('/<serie>/<numero>', methods=['PUT'])
def modificar_credencial(serie, numero):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE credencial SET ci_ciudadano = %s WHERE serie = %s AND numero = %s",
                   (data['ci_ciudadano'], serie, numero))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Credencial modificada'})

@credencial_bp.route('/<serie>/<numero>', methods=['DELETE'])
def eliminar_credencial(serie, numero):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM credencial WHERE serie = %s AND numero = %s", (serie, numero))
        conn.commit()
        return jsonify({'mensaje': 'Credencial eliminada'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar credencial: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()
