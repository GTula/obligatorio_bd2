
from flask import Blueprint, request, jsonify
from db import get_db_connection

ciudadano_bp = Blueprint('ciudadano', __name__)

# -------------------- Ciudadano --------------------
@ciudadano_bp.route('/ciudadanos', methods=['GET'])
def listar_ciudadanos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ciudadano")
    ciudadanos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(ciudadanos)

@ciudadano_bp.route('/ciudadano', methods=['POST'])
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

@ciudadano_bp.route('/ciudadano/<ci>', methods=['PUT'])
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

@ciudadano_bp.route('/ciudadano/<ci>', methods=['DELETE'])
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


@ciudadano_bp.route('/ciudadano/forzar/<ci>', methods=['DELETE'])
def forzar_eliminar_ciudadano(ci):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Eliminaciones con parámetros correctos
        eliminaciones = [
            ("DELETE FROM participacion_en_mesa WHERE ci_ciudadano = %s", (ci,)),
            
            ("DELETE FROM agente_establecimiento WHERE ci_policia = %s", (ci,)),
            
            ("DELETE FROM vota_en WHERE serie_credencial IN (SELECT serie FROM credencial WHERE ci_ciudadano = %s) AND numero_credencial IN (SELECT numero FROM credencial WHERE ci_ciudadano = %s)", (ci, ci)),
            
            ("DELETE FROM asignado WHERE serie_credencial IN (SELECT serie FROM credencial WHERE ci_ciudadano = %s) AND numero_credencial IN (SELECT numero FROM credencial WHERE ci_ciudadano = %s)", (ci, ci)),
            
            ("DELETE FROM candidato_por_lista WHERE id_candidato = %s", (ci,)),
            ("DELETE FROM autoridad WHERE ci_ciudadano = %s", (ci,)),
            ("DELETE FROM agente_policia WHERE ci_ciudadano = %s", (ci,)),
            ("DELETE FROM empleado_publico WHERE ci_ciudadano = %s", (ci,)),
            ("DELETE FROM candidato WHERE ci_ciudadano = %s", (ci,)),
            
            ("DELETE FROM credencial WHERE ci_ciudadano = %s", (ci,)),
            
            ("DELETE FROM ciudadano WHERE ci = %s", (ci,))
        ]
        
        for sql, params in eliminaciones:
            try:
                cursor.execute(sql, params)
                print(f"Ejecutado: {sql} con parámetros: {params}")
            except Exception as e:
                print(f"Warning en eliminación: {sql} - {str(e)}")
                continue
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        return jsonify({'mensaje': 'Ciudadano eliminado forzadamente con todas sus dependencias'})
        
    except Exception as e:
        conn.rollback()
        print(f"Error completo: {str(e)}")
        return jsonify({'error': f'Error en eliminación forzada: {str(e)}'}), 400
    finally:
        cursor.close()
        conn.close()
