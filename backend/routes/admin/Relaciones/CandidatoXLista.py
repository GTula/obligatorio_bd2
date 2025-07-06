
from flask import Blueprint, request, jsonify
from db import get_db_connection

candidato_por_lista_bp = Blueprint('candidato-por-lista', __name__)


# -------------------- Candidato por Lista --------------------
@candidato_por_lista_bp.route('/candidatos-por-lista', methods=['GET'])
def listar_candidatos_por_lista():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM candidato_por_lista")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@candidato_por_lista_bp.route('/candidato-por-lista', methods=['POST'])
def crear_candidato_por_lista():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO candidato_por_lista (id_papeleta, id_eleccion, id_candidato) VALUES (%s, %s, %s)",
               (data['id_papeleta'], data['id_eleccion'], data['id_candidato']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Candidato por lista creado'})

@candidato_por_lista_bp.route('/candidato-por-lista/<int:id_papeleta>/<int:id_eleccion>/<id_candidato>', methods=['PUT'])
def modificar_candidato_por_lista(id_papeleta, id_eleccion, id_candidato):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE candidato_por_lista SET id_candidato = %s WHERE id_papeleta = %s AND id_eleccion = %s AND id_candidato = %s",
                   (data['id_candidato'], id_papeleta, id_eleccion, id_candidato))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Candidato por lista modificado'})

@candidato_por_lista_bp.route('/candidato-por-lista/<int:id_papeleta>/<int:id_eleccion>/<id_candidato>', methods=['DELETE'])
def eliminar_candidato_por_lista(id_papeleta, id_eleccion, id_candidato):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM candidato_por_lista WHERE id_papeleta = %s AND id_eleccion = %s AND id_candidato = %s",
                   (id_papeleta, id_eleccion, id_candidato))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Candidato por lista eliminado'})

