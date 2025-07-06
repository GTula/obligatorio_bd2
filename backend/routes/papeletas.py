from flask import Blueprint, jsonify, request
from db import get_db_connection

papeletas_bp = Blueprint("papeletas", __name__)

@papeletas_bp.route('/eleccion/<int:id_eleccion>', methods=['GET'])
def get_papeletas_eleccion(id_eleccion):
    """Obtener papeletas disponibles para una elección"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        # Primero verificar el tipo de elección
        cursor.execute("""
            SELECT e.id, e.fecha, te.nombre as tipo_eleccion, e.id_tipo_eleccion
            FROM eleccion e
            JOIN tipo_eleccion te ON e.id_tipo_eleccion = te.id
            WHERE e.id = %s
        """, (id_eleccion,))
        
        eleccion = cursor.fetchone()
        if not eleccion:
            return jsonify({"error": "Elección no encontrada"}), 404

        papeletas = []
        
        if eleccion['id_tipo_eleccion'] == 3:  # Plebiscito
            cursor.execute("""
                SELECT p.id, p.id_eleccion, pp.nombre, pp.valor
                FROM papeleta p
                JOIN papeleta_plebiscito pp ON p.id = pp.id_papeleta AND p.id_eleccion = pp.id_eleccion
                WHERE p.id_eleccion = %s
                ORDER BY pp.valor
            """, (id_eleccion,))
            
            papeletas = cursor.fetchall()
            
        else:  # Otras elecciones (con listas y partidos)
            cursor.execute("""
                SELECT p.id, p.id_eleccion, l.organo, pt.nombre as partido, pt.id as id_partido,
                       d.nombre as departamento
                FROM papeleta p
                JOIN lista l ON p.id = l.id_papeleta AND p.id_eleccion = l.id_eleccion
                JOIN partido pt ON l.id_partido = pt.id
                JOIN departamento d ON l.id_departamento = d.id
                WHERE p.id_eleccion = %s
                ORDER BY pt.nombre, l.organo
            """, (id_eleccion,))
            
            papeletas = cursor.fetchall()

        return jsonify({
            "eleccion": eleccion,
            "papeletas": papeletas
        })
        
    except Exception as e:
        print(f"Error obteniendo papeletas: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@papeletas_bp.route('/votar', methods=['POST'])
def registrar_voto():
    """Registrar un voto en el sistema"""
    data = request.json
    
    required_fields = ['id_circuito', 'id_eleccion', 'tipo_voto', 'observado']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Crear registro base de voto
        cursor.execute("""
            INSERT INTO voto (id_circuito, id_eleccion, observado)
            VALUES (%s, %s, %s)
        """, (data['id_circuito'], data['id_eleccion'], data['observado']))
        
        voto_id = cursor.lastrowid

        # Registrar según el tipo de voto
        if data['tipo_voto'] == 'anulado':
            cursor.execute("INSERT INTO voto_anulado (id_voto) VALUES (%s)", (voto_id,))
            
        elif data['tipo_voto'] == 'blanco':
            cursor.execute("INSERT INTO voto_blanco (id_voto) VALUES (%s)", (voto_id,))
            
        elif data['tipo_voto'] == 'normal':
            # Verificar que se haya seleccionado una papeleta
            if 'id_papeleta' not in data:
                return jsonify({"error": "Debe seleccionar una papeleta para voto normal"}), 400
                
            cursor.execute("""
                INSERT INTO voto_normal (id_voto, observado) 
                VALUES (%s, %s)
            """, (voto_id, data['observado']))
            
            cursor.execute("""
                INSERT INTO voto_elige_papeleta (id_voto_normal, id_papeleta, id_eleccion)
                VALUES (%s, %s, %s)
            """, (voto_id, data['id_papeleta'], data['id_eleccion']))
        
        conn.commit()
        
        return jsonify({
            "mensaje": "Voto registrado exitosamente",
            "voto_id": voto_id,
            "tipo_voto": data['tipo_voto']
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error registrando voto: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
