# -------------------- Voto --------------------
@admin_bp.route('/votos', methods=['GET'])
def listar_votos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM voto")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/voto', methods=['POST'])
def crear_voto():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO voto (id_circuito, id_eleccion, observado) VALUES (%s, %s, %s)",
                   (data['id_circuito'], data['id_eleccion'], data.get('observado', 0)))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto creado'})

@admin_bp.route('/voto/<int:id>', methods=['PUT'])
def modificar_voto(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE voto SET id_circuito = %s, id_eleccion = %s, observado = %s WHERE id = %s",
                   (data['id_circuito'], data['id_eleccion'], data['observado'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto modificado'})

@admin_bp.route('/voto/<int:id>', methods=['DELETE'])
def eliminar_voto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM voto WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Voto eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar voto: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()
