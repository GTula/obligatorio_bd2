
from flask import Blueprint, request, jsonify
from db import get_db_connection

empleado_publico_bp = Blueprint('empleado-publico', __name__)


# -------------------- Empleado Público (continuación) --------------------
@empleado_publico_bp.route('/empleados-publicos', methods=['GET'])
def listar_empleados_publicos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ep.ci_ciudadano, ci.nombre, ci.apellido, ep.num_mesa, ep.id_tipo, te.nombre as tipo_nombre
        FROM empleado_publico ep 
        JOIN ciudadano ci ON ep.ci_ciudadano = ci.ci
        LEFT JOIN tipo_empleado te ON ep.id_tipo = te.id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@empleado_publico_bp.route('/empleado-publico', methods=['POST'])
def crear_empleado_publico():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Verificar que el ciudadano existe
        cursor.execute("SELECT ci FROM ciudadano WHERE ci = %s", (data['ci_ciudadano'],))
        if not cursor.fetchone():
            return jsonify({'error': 'El ciudadano no existe'}), 400
            
        cursor.execute("INSERT INTO empleado_publico (ci_ciudadano, num_mesa, id_tipo) VALUES (%s, %s, %s)",
                       (data['ci_ciudadano'], data.get('num_mesa'), data.get('id_tipo')))
        conn.commit()
        return jsonify({'mensaje': 'Empleado público creado'})
    except Exception as e:
        return jsonify({'error': f'Error creando empleado público: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()

@empleado_publico_bp.route('/empleados-publicos/<ci>', methods=['PUT'])
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

@empleado_publico_bp.route('/empleados-publicos/<ci>', methods=['DELETE'])
def eliminar_empleado_publico(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleado_publico WHERE ci_ciudadano = %s", (ci,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Empleado público eliminado'})