from flask import Blueprint, request, jsonify
from db import get_db_connection

admin_bp = Blueprint('admin', __name__)

# -------------------- Ciudadano --------------------
@admin_bp.route('/ciudadanos', methods=['GET'])
def listar_ciudadanos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ciudadano")
    ciudadanos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(ciudadanos)

@admin_bp.route('/ciudadano', methods=['POST'])
def crear_ciudadano():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ciudadano (ci, nombre, apellido, fecha_nac) VALUES (%s, %s, %s, %s)",
                   (data['ci'], data['nombre'], data['apellido'], data['fecha_nac']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Ciudadano creado'}), 201

@admin_bp.route('/ciudadano/<ci>', methods=['PUT'])
def editar_ciudadano(ci):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE ciudadano SET nombre = %s, apellido = %s, fecha_nac = %s WHERE ci = %s",
                       (data['nombre'], data['apellido'], data['fecha_nac'], ci))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Ciudadano actualizado'})
    except Exception as e:
        return jsonify({'error': f'Error updating ciudadano: {str(e)}'}), 500

@admin_bp.route('/ciudadano/<ci>', methods=['DELETE'])
def eliminar_ciudadano(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ciudadano WHERE ci = %s", (ci,))
        conn.commit()
        return jsonify({'mensaje': 'Ciudadano eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar ciudadano: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@admin_bp.route('/ciudadano/forzar/<ci>', methods=['DELETE'])
def forzar_eliminar_ciudadano(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM ciudadano WHERE ci = %s", (ci,))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Ciudadano eliminado forzadamente'})
    finally:
        cursor.close()
        conn.close()

# -------------------- Departamento --------------------
@admin_bp.route('/departamentos', methods=['GET'])
def listar_departamentos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM departamento")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/departamento', methods=['POST'])
def crear_departamento():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO departamento (nombre) VALUES (%s)", (data['nombre'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Departamento creado'})

@admin_bp.route('/departamento/<int:id>', methods=['PUT'])
def modificar_departamento(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE departamento SET nombre = %s WHERE id = %s", (data['nombre'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Departamento modificado'})

@admin_bp.route('/departamento/<int:id>', methods=['DELETE'])
def eliminar_departamento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM zona WHERE id_departamento = %s", (id,))
        if cursor.fetchone():
            return jsonify({'error': 'No se puede eliminar un departamento con zonas asociadas'}), 400
        cursor.execute("DELETE FROM departamento WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Departamento eliminado'})
    finally:
        cursor.close()
        conn.close()

# -------------------- Comisaria --------------------
@admin_bp.route('/comisarias', methods=['GET'])
def listar_comisarias():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM comisaria")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/comisaria', methods=['POST'])
def crear_comisaria():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comisaria (nombre) VALUES (%s)", (data['nombre'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Comisaría creada'})

@admin_bp.route('/comisaria/<int:id>', methods=['PUT'])
def modificar_comisaria(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE comisaria SET nombre = %s WHERE id = %s", (data['nombre'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Comisaría modificada'})

@admin_bp.route('/comisaria/<int:id>', methods=['DELETE'])
def eliminar_comisaria(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comisaria WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Comisaría eliminada'})

# -------------------- Partido --------------------
@admin_bp.route('/partidos', methods=['GET'])
def listar_partidos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM partido")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/partido', methods=['POST'])
def crear_partido():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO partido (nombre, direccion) VALUES (%s, %s)",
                   (data['nombre'], data['direccion']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Partido creado'})

@admin_bp.route('/partido/<int:id>', methods=['PUT'])
def modificar_partido(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE partido SET nombre = %s, direccion = %s WHERE id = %s",
                   (data['nombre'], data['direccion'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Partido modificado'})

@admin_bp.route('/partido/<int:id>', methods=['DELETE'])
def eliminar_partido(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM partido WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Partido eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar partido: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# -------------------- Establecimiento --------------------
@admin_bp.route('/establecimientos', methods=['GET'])
def listar_establecimientos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM establecimiento")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/establecimiento', methods=['POST'])
def crear_establecimiento():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO establecimiento (direccion, id_zona, id_departamento) VALUES (%s, %s, %s)",
                   (data['direccion'], data['id_zona'], data['id_departamento']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Establecimiento creado'})

@admin_bp.route('/establecimiento/<int:id>', methods=['PUT'])
def modificar_establecimiento(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE establecimiento SET direccion = %s, id_zona = %s, id_departamento = %s WHERE id = %s",
                   (data['direccion'], data['id_zona'], data['id_departamento'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Establecimiento modificado'})

@admin_bp.route('/establecimiento/<int:id>', methods=['DELETE'])
def eliminar_establecimiento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM circuito WHERE id_establecimiento = %s", (id,))
        if cursor.fetchone():
            return jsonify({'error': 'No se puede eliminar establecimiento asociado a circuito'}), 400
        cursor.execute("DELETE FROM establecimiento WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Establecimiento eliminado'})
    finally:
        cursor.close()
        conn.close()

# -------------------- Zona --------------------
@admin_bp.route('/zonas', methods=['GET'])
def listar_zonas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM zona")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/zona', methods=['POST'])
def crear_zona():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO zona (nombre, id_departamento) VALUES (%s, %s)",
                   (data['nombre'], data['id_departamento']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Zona creada'})

@admin_bp.route('/zona/<int:id>/<int:id_departamento>', methods=['PUT'])
def modificar_zona(id, id_departamento):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE zona SET nombre = %s WHERE id = %s AND id_departamento = %s",
                   (data['nombre'], id, id_departamento))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Zona modificada'})

@admin_bp.route('/zona/<int:id>/<int:id_departamento>', methods=['DELETE'])
def eliminar_zona(id, id_departamento):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM establecimiento WHERE id_zona = %s AND id_departamento = %s", (id, id_departamento))
        if cursor.fetchone():
            return jsonify({'error': 'No se puede eliminar zona con establecimientos asociados'}), 400
        cursor.execute("DELETE FROM zona WHERE id = %s AND id_departamento = %s", (id, id_departamento))
        conn.commit()
        return jsonify({'mensaje': 'Zona eliminada'})
    finally:
        cursor.close()
        conn.close()






# -------------------- Candidato (continuación) --------------------
@admin_bp.route('/candidato', methods=['POST'])
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

@admin_bp.route('/candidato/<ci>', methods=['PUT'])
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

@admin_bp.route('/candidato/<ci>', methods=['DELETE'])
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

# -------------------- Autoridad --------------------
@admin_bp.route('/autoridades', methods=['GET'])
def listar_autoridades():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM autoridad")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/autoridad', methods=['POST'])
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

@admin_bp.route('/autoridad/<ci>', methods=['PUT'])
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

@admin_bp.route('/autoridad/<ci>', methods=['DELETE'])
def eliminar_autoridad(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM autoridad WHERE ci_ciudadano = %s", (ci,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Autoridad eliminada'})

# -------------------- Credencial --------------------
@admin_bp.route('/credenciales', methods=['GET'])
def listar_credenciales():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM credencial")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/credencial', methods=['POST'])
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

@admin_bp.route('/credencial/<serie>/<numero>', methods=['PUT'])
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

@admin_bp.route('/credencial/<serie>/<numero>', methods=['DELETE'])
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

# -------------------- Elección --------------------
@admin_bp.route('/elecciones', methods=['GET'])
def listar_elecciones():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM eleccion")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/eleccion', methods=['POST'])
def crear_eleccion():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO eleccion (fecha, id_tipo_eleccion) VALUES (%s, %s)",
                   (data['fecha'], data['id_tipo_eleccion']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Elección creada'})

@admin_bp.route('/eleccion/<int:id>', methods=['PUT'])
def modificar_eleccion(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE eleccion SET fecha = %s, id_tipo_eleccion = %s WHERE id = %s",
                   (data['fecha'], data['id_tipo_eleccion'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Elección modificada'})

@admin_bp.route('/eleccion/<int:id>', methods=['DELETE'])
def eliminar_eleccion(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM eleccion WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Elección eliminada'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar elección: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# -------------------- Agente Policía --------------------
@admin_bp.route('/agentes-policia', methods=['GET'])
def listar_agentes_policia():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agente_policia")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/agente-policia', methods=['POST'])
def crear_agente_policia():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO agente_policia (ci_ciudadano, id_comisaria) VALUES (%s, %s)",
                   (data['ci_ciudadano'], data['id_comisaria']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Agente de policía creado'})

@admin_bp.route('/agente-policia/<ci>', methods=['PUT'])
def modificar_agente_policia(ci):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE agente_policia SET id_comisaria = %s WHERE ci_ciudadano = %s",
                   (data['id_comisaria'], ci))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Agente de policía modificado'})

@admin_bp.route('/agente-policia/<ci>', methods=['DELETE'])
def eliminar_agente_policia(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM agente_policia WHERE ci_ciudadano = %s", (ci,))
        conn.commit()
        return jsonify({'mensaje': 'Agente de policía eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar agente de policía: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# -------------------- Circuito --------------------
@admin_bp.route('/circuitos', methods=['GET'])
def listar_circuitos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM circuito")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/circuito', methods=['POST'])
def crear_circuito():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO circuito (id_eleccion, accesible, id_establecimiento) VALUES (%s, %s, %s)",
                   (data['id_eleccion'], data['accesible'], data['id_establecimiento']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Circuito creado'})

@admin_bp.route('/circuito/<int:id>/<int:id_eleccion>', methods=['PUT'])
def modificar_circuito(id, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE circuito SET accesible = %s, id_establecimiento = %s WHERE id = %s AND id_eleccion = %s",
                   (data['accesible'], data['id_establecimiento'], id, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Circuito modificado'})

@admin_bp.route('/circuito/<int:id>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_circuito(id, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM circuito WHERE id = %s AND id_eleccion = %s", (id, id_eleccion))
        conn.commit()
        return jsonify({'mensaje': 'Circuito eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar circuito: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# -------------------- Mesa --------------------
@admin_bp.route('/mesas', methods=['GET'])
def listar_mesas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mesa")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/mesa', methods=['POST'])
def crear_mesa():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mesa (num, id_circuito, id_eleccion) VALUES (%s, %s, %s)",
                   (data['num'], data['id_circuito'], data['id_eleccion']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Mesa creada'})

@admin_bp.route('/mesa/<int:num>', methods=['PUT'])
def modificar_mesa(num):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE mesa SET id_circuito = %s, id_eleccion = %s WHERE num = %s",
                   (data['id_circuito'], data['id_eleccion'], num))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Mesa modificada'})

@admin_bp.route('/mesa/<int:num>', methods=['DELETE'])
def eliminar_mesa(num):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM mesa WHERE num = %s", (num,))
        conn.commit()
        return jsonify({'mensaje': 'Mesa eliminada'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar mesa: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()







# -------------------- Empleado Público (continuación) --------------------
@admin_bp.route('/empleado-publico/<ci>', methods=['PUT'])
def modificar_empleado_publico(ci):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE empleado_publico SET num_mesa = %s, id_tipo = %s WHERE ci_ciudadano = %s",
                   (data['num_mesa'], data['id_tipo'], ci))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Empleado público modificado'})

@admin_bp.route('/empleado-publico/<ci>', methods=['DELETE'])
def eliminar_empleado_publico(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleado_publico WHERE ci_ciudadano = %s", (ci,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Empleado público eliminado'})

# -------------------- Asignado --------------------
@admin_bp.route('/asignados', methods=['GET'])
def listar_asignados():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM asignado")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/asignado', methods=['POST'])
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

@admin_bp.route('/asignado/<serie>/<numero>/<int:id_circuito>/<int:id_eleccion>', methods=['PUT'])
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

@admin_bp.route('/asignado/<serie>/<numero>/<int:id_circuito>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_asignado(serie, numero, id_circuito, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM asignado WHERE serie_credencial = %s AND numero_credencial = %s AND id_circuito = %s AND id_eleccion = %s",
                   (serie, numero, id_circuito, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Asignación eliminada'})

# -------------------- Vota En --------------------
@admin_bp.route('/vota-en', methods=['GET'])
def listar_vota_en():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vota_en")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/vota-en', methods=['POST'])
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

@admin_bp.route('/vota-en/<serie>/<numero>/<int:id_circuito>/<int:id_eleccion>', methods=['PUT'])
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

@admin_bp.route('/vota-en/<serie>/<numero>/<int:id_circuito>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_vota_en(serie, numero, id_circuito, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vota_en WHERE serie_credencial = %s AND numero_credencial = %s AND id_circuito = %s AND id_eleccion = %s",
                   (serie, numero, id_circuito, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto eliminado'})

# -------------------- Papeleta --------------------
@admin_bp.route('/papeletas', methods=['GET'])
def listar_papeletas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM papeleta")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/papeleta', methods=['POST'])
def crear_papeleta():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO papeleta (id_eleccion) VALUES (%s)",
                   (data['id_eleccion'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Papeleta creada'})

@admin_bp.route('/papeleta/<int:id>/<int:id_eleccion>', methods=['PUT'])
def modificar_papeleta(id, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE papeleta SET id_eleccion = %s WHERE id = %s AND id_eleccion = %s",
                   (data['id_eleccion'], id, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Papeleta modificada'})

@admin_bp.route('/papeleta/<int:id>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_papeleta(id, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM papeleta WHERE id = %s AND id_eleccion = %s", (id, id_eleccion))
        conn.commit()
        return jsonify({'mensaje': 'Papeleta eliminada'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar papeleta: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# -------------------- Lista --------------------
@admin_bp.route('/listas', methods=['GET'])
def listar_listas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lista")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/lista', methods=['POST'])
def crear_lista():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lista (id_papeleta, id_eleccion, id_partido, organo, id_departamento) VALUES (%s, %s, %s, %s, %s)",
                   (data['id_papeleta'], data['id_eleccion'], data['id_partido'], data['organo'], data['id_departamento']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Lista creada'})

@admin_bp.route('/lista/<int:id_papeleta>/<int:id_eleccion>', methods=['PUT'])
def modificar_lista(id_papeleta, id_eleccion):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE lista SET id_partido = %s, organo = %s, id_departamento = %s WHERE id_papeleta = %s AND id_eleccion = %s",
                   (data['id_partido'], data['organo'], data['id_departamento'], id_papeleta, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Lista modificada'})

@admin_bp.route('/lista/<int:id_papeleta>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_lista(id_papeleta, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM lista WHERE id_papeleta = %s AND id_eleccion = %s", (id_papeleta, id_eleccion))
        conn.commit()
        return jsonify({'mensaje': 'Lista eliminada'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar lista: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# -------------------- Candidato por Lista --------------------
@admin_bp.route('/candidatos-por-lista', methods=['GET'])
def listar_candidatos_por_lista():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM candidato_por_lista")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/candidato-por-lista', methods=['POST'])
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

@admin_bp.route('/candidato-por-lista/<int:id_papeleta>/<int:id_eleccion>/<id_candidato>', methods=['PUT'])
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

@admin_bp.route('/candidato-por-lista/<int:id_papeleta>/<int:id_eleccion>/<id_candidato>', methods=['DELETE'])
def eliminar_candidato_por_lista(id_papeleta, id_eleccion, id_candidato):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM candidato_por_lista WHERE id_papeleta = %s AND id_eleccion = %s AND id_candidato = %s",
                   (id_papeleta, id_eleccion, id_candidato))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Candidato por lista eliminado'})







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

# -------------------- Tipo Elección --------------------
@admin_bp.route('/tipos-eleccion', methods=['GET'])
def listar_tipos_eleccion():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tipo_eleccion")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/tipo-eleccion', methods=['POST'])
def crear_tipo_eleccion():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tipo_eleccion (nombre) VALUES (%s)", (data['nombre'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Tipo de elección creado'})

@admin_bp.route('/tipo-eleccion/<int:id>', methods=['PUT'])
def modificar_tipo_eleccion(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tipo_eleccion SET nombre = %s WHERE id = %s", (data['nombre'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Tipo de elección modificado'})

@admin_bp.route('/tipo-eleccion/<int:id>', methods=['DELETE'])
def eliminar_tipo_eleccion(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tipo_eleccion WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Tipo de elección eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar tipo de elección: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# -------------------- Tipo Empleado --------------------
@admin_bp.route('/tipos-empleado', methods=['GET'])
def listar_tipos_empleado():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tipo_empleado")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/tipo-empleado', methods=['POST'])
def crear_tipo_empleado():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tipo_empleado (nombre) VALUES (%s)", (data['nombre'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Tipo de empleado creado'})

@admin_bp.route('/tipo-empleado/<int:id>', methods=['PUT'])
def modificar_tipo_empleado(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tipo_empleado SET nombre = %s WHERE id = %s", (data['nombre'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Tipo de empleado modificado'})

@admin_bp.route('/tipo-empleado/<int:id>', methods=['DELETE'])
def eliminar_tipo_empleado(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tipo_empleado WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'mensaje': 'Tipo de empleado eliminado'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar tipo de empleado: ' + str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# -------------------- Agente Establecimiento --------------------
@admin_bp.route('/agentes-establecimiento', methods=['GET'])
def listar_agentes_establecimiento():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agente_establecimiento")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/agente-establecimiento', methods=['POST'])
def crear_agente_establecimiento():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO agente_establecimiento (ci_policia, id_establecimiento) VALUES (%s, %s)",
                   (data['ci_policia'], data['id_establecimiento']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Agente establecimiento creado'})

@admin_bp.route('/agente-establecimiento/<ci>/<int:id_establecimiento>', methods=['PUT'])
def modificar_agente_establecimiento(ci, id_establecimiento):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE agente_establecimiento SET id_establecimiento = %s WHERE ci_policia = %s AND id_establecimiento = %s",
                   (data['id_establecimiento'], ci, id_establecimiento))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Agente establecimiento modificado'})

@admin_bp.route('/agente-establecimiento/<ci>/<int:id_establecimiento>', methods=['DELETE'])
def eliminar_agente_establecimiento(ci, id_establecimiento):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agente_establecimiento WHERE ci_policia = %s AND id_establecimiento = %s",
                   (ci, id_establecimiento))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Agente establecimiento eliminado'})

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

# -------------------- Voto Anulado --------------------
@admin_bp.route('/votos-anulados', methods=['GET'])
def listar_votos_anulados():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM voto_anulado")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/voto-anulado', methods=['POST'])
def crear_voto_anulado():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO voto_anulado (id_voto) VALUES (%s)", (data['id_voto'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto anulado creado'})

@admin_bp.route('/voto-anulado/<int:id_voto>', methods=['DELETE'])
def eliminar_voto_anulado(id_voto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM voto_anulado WHERE id_voto = %s", (id_voto,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto anulado eliminado'})

# -------------------- Voto Blanco --------------------
@admin_bp.route('/votos-blancos', methods=['GET'])
def listar_votos_blancos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM voto_blanco")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/voto-blanco', methods=['POST'])
def crear_voto_blanco():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO voto_blanco (id_voto) VALUES (%s)", (data['id_voto'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto blanco creado'})

@admin_bp.route('/voto-blanco/<int:id_voto>', methods=['DELETE'])
def eliminar_voto_blanco(id_voto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM voto_blanco WHERE id_voto = %s", (id_voto,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto blanco eliminado'})

# -------------------- Voto Normal --------------------
@admin_bp.route('/votos-normales', methods=['GET'])
def listar_votos_normales():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM voto_normal")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@admin_bp.route('/voto-normal', methods=['POST'])
def crear_voto_normal():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO voto_normal (id_voto, observado) VALUES (%s, %s)",
                   (data['id_voto'], data.get('observado', 0)))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto normal creado'})

@admin_bp.route('/voto-normal/<int:id_voto>', methods=['PUT'])
def modificar_voto_normal(id_voto):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE voto_normal SET observado = %s WHERE id_voto = %s",
                   (data['observado'], id_voto))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto normal modificado'})

@admin_bp.route('/voto-normal/<int:id_voto>', methods=['DELETE'])
def eliminar_voto_normal(id_voto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM voto_normal WHERE id_voto = %s", (id_voto,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Voto normal eliminado'})






# -------------------- Papeleta Plebiscito (continuación) --------------------
@admin_bp.route('/papeleta-plebiscito', methods=['POST'])
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

@admin_bp.route('/papeleta-plebiscito/<int:id_papeleta>/<int:id_eleccion>', methods=['PUT'])
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

@admin_bp.route('/papeleta-plebiscito/<int:id_papeleta>/<int:id_eleccion>', methods=['DELETE'])
def eliminar_papeleta_plebiscito(id_papeleta, id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM papeleta_plebiscito WHERE id_papeleta = %s AND id_eleccion = %s",
                   (id_papeleta, id_eleccion))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Papeleta plebiscito eliminada'})