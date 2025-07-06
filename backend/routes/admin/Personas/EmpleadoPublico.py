
from flask import Blueprint, request, jsonify
from db import get_db_connection

empleado_publico_bp = Blueprint('empleado-publico', __name__)


# -------------------- Empleado Público (continuación) --------------------
@empleado_publico_bp.route('/empleados-publicos', methods=['GET'])
def listar_empleados_publicos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ep.ci_ciudadano, ci.nombre, ci.apellido
        FROM empleado_publico ep 
        JOIN ciudadano ci ON ep.ci_ciudadano = ci.ci
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
            
        cursor.execute("INSERT INTO empleado_publico (ci_ciudadano) VALUES (%s)",
                       (data['ci_ciudadano'],))
        conn.commit()
        return jsonify({'mensaje': 'Empleado público creado'})
    except Exception as e:
        return jsonify({'error': f'Error creando empleado público: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()


@empleado_publico_bp.route('/empleado-publico/<ci>', methods=['DELETE'])
def eliminar_empleado_publico(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleado_publico WHERE ci_ciudadano = %s", (ci,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Empleado público eliminado'})

@empleado_publico_bp.route('/empleado-publico/forzar/<ci_ciudadano>', methods=['DELETE'])
def forzar_eliminar_empleado_publico(ci_ciudadano):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM participacion_en_mesa WHERE ci_ciudadano = %s", (ci_ciudadano,))
        cursor.execute("DELETE FROM empleado_publico WHERE ci_ciudadano = %s", (ci_ciudadano,))
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Empleado público eliminado forzadamente'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
