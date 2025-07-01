from flask import Blueprint, request, jsonify
from db import get_db_connection

vota_en_bp = Blueprint('vota-en', __name__)


# -------------------- Vota En --------------------
@vota_en_bp.route('/vota-en', methods=['GET'])
def listar_vota_en():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vota_en")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@vota_en_bp.route('/vota-en', methods=['POST'])
def crear_vota_en():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vota_en (serie_credencial, numero_credencial, id_circuito, id_eleccion, observado) VALUES (%s, %s, %s, %s, %s)",
                   (data['serie_credencial'], data['numero_credencial'], data['id_circuito'], data['id_eleccion'], data.get('observado', 0)))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto registrado'})

@vota_en_bp.route('/vota-en/<serie>/<numero>/<int:id_circuito>/<int:id_eleccion>', methods=['PUT'])
def modificar_vota_en(serie, numero, id_circuito, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE vota_en SET observado = %s WHERE serie_credencial = %s AND numero_credencial = %s AND id_circuito = %s AND id_eleccion = %s",
                   (data['observado'], serie, numero, id_circuito, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto modificado'})

@vota_en_bp.route('/vota-en/<serie>/<numero>/<int:id_circuito>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_vota_en(serie, numero, id_circuito, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vota_en WHERE serie_credencial = %s AND numero_credencial = %s AND id_circuito = %s AND id_eleccion = %s",
                   (serie, numero, id_circuito, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto eliminado'})