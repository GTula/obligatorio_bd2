
from flask import Blueprint, request, jsonify
from db import get_db_connection

papeleta_plebiscito_bp = Blueprint('papeleta_plebiscito', __name__)

# -------------------- Papeleta Plebiscito (continuación) --------------------
@papeleta_plebiscito_bp.route('', methods=['POST'])
def crear_papeleta_plebiscito():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO papeleta_plebiscito (id_papeleta, id_eleccion, nombre, valor) VALUES (%s, %s, %s, %s)",
                   (data['id_papeleta'], data['id_eleccion'], data['nombre'], data['valor']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Papeleta plebiscito creada'})

@papeleta_plebiscito_bp.route('/<int:id_papeleta>/<int:id_eleccion>', methods=['PUT'])
def modificar_papeleta_plebiscito(id_papeleta, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE papeleta_plebiscito SET nombre = %s, valor = %s WHERE id_papeleta = %s AND id_eleccion = %s",
                   (data['nombre'], data['valor'], id_papeleta, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Papeleta plebiscito modificada'})

@papeleta_plebiscito_bp.route('/<int:id_papeleta>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_papeleta_plebiscito(id_papeleta, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s",
                   (id_papeleta, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Papeleta plebiscito eliminada'})