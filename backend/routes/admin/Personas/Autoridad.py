
from flask import Blueprint, request, jsonify
from db import get_db_connection

autoridad_bp = Blueprint('autoridad', __name__)


# -------------------- Autoridad --------------------
@autoridad_bp.route('/autoridades', methods=['GET'])
def listar_autoridades():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM autoridad")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@autoridad_bp.route('/autoridad', methods=['POST'])
def crear_autoridad():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO autoridad (ci_ciudadano, id_partido) VALUES (%s, %s)",
                   (data['ci_ciudadano'], data['id_partido']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Autoridad creada'})

@autoridad_bp.route('/autoridad/<ci>', methods=['PUT'])
def modificar_autoridad(ci):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE autoridad SET id_partido = %s WHERE ci_ciudadano = %s",
                   (data['id_partido'], ci))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Autoridad modificada'})

@autoridad_bp.route('/autoridad/<ci>', methods=['DELETE'])
def eliminar_autoridad(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM autoridad WHERE ci_ciudadano = %s", (ci,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Autoridad eliminada'})