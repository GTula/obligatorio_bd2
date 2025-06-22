
from flask import Blueprint, request, jsonify
from db import get_db_connection

empleado_publico_bp = Blueprint('empleado_publico', __name__)


# -------------------- Empleado Público (continuación) --------------------
@empleado_publico_bp.route('/<ci>', methods=['PUT'])
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

@empleado_publico_bp.route('/<ci>', methods=['DELETE'])
def eliminar_empleado_publico(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleado_publico WHERE ci_ciudadano = %s", (ci,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Empleado público eliminado'})