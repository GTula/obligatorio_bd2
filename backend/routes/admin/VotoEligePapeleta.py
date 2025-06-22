# -------------------- Voto Elige Papeleta (continuación) --------------------
@admin_bp.route('/voto-elige-papeleta/<int:id_voto_normal>/<int:id_papeleta>/<int:id_eleccion>', methods=['PUT'])
def modificar_voto_elige_papeleta(id_voto_normal, id_papeleta, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE voto_elige_papeleta SET id_papeleta = %s, id_eleccion = %s WHERE id_voto_normal = %s AND id_papeleta = %s AND id_eleccion = %s",
                   (data['id_papeleta'], data['id_eleccion'], id_voto_normal, id_papeleta, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto elige papeleta modificado'})

@admin_bp.route('/voto-elige-papeleta/<int:id_voto_normal>/<int:id_papeleta>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_voto_elige_papeleta(id_voto_normal, id_papeleta, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM voto_elige_papeleta WHERE id_voto_normal = %s AND id_papeleta = %s AND id_eleccion = %s",
                   (id_voto_normal, id_papeleta, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto elige papeleta eliminado'})

