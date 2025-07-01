
from flask import Blueprint, request, jsonify
from db import get_db_connection

asignado_bp = Blueprint('asignado', __name__)


# -------------------- Asignado --------------------
@asignado_bp.route('/asignados', methods=['GET'])
def listar_asignados():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM asignado")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@asignado_bp.route('/asignado', methods=['POST'])
def crear_asignado():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO asignado (serie_credencial, numero_credencial, id_circuito, id_eleccion) VALUES (%s, %s, %s, %s)",
                   (data['serie_credencial'], data['numero_credencial'], data['id_circuito'], data['id_eleccion']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Asignación creada'})

@asignado_bp.route('/asignado/<serie>/<numero>/<int:id_circuito>/<int:id_eleccion>', methods=['PUT'])
def modificar_asignado(serie, numero, id_circuito, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE asignado SET id_circuito = %s, id_eleccion = %s WHERE serie_credencial = %s AND numero_credencial = %s AND id_circuito = %s AND id_eleccion = %s",
                   (data['id_circuito'], data['id_eleccion'], serie, numero, id_circuito, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Asignación modificada'})

@asignado_bp.route('/asignado/<serie>/<numero>/<int:id_circuito>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_asignado(serie, numero, id_circuito, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM asignado WHERE serie_credencial = %s AND numero_credencial = %s AND id_circuito = %s AND id_eleccion = %s",
                   (serie, numero, id_circuito, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Asignación eliminada'})