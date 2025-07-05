from flask import Blueprint, jsonify, request
from db import get_db_connection

votos_bp = Blueprint("votos", __name__)

@votos_bp.route('/<int:num_mesa>/votos_normales/<int:id_eleccion>', methods=['GET'])
def get_votos_normales(num_mesa, id_eleccion):
    fecha = request.args.get('fecha')
    
    
    if not fecha:
        return jsonify({"error": "Falta el parámetro 'fecha'"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        # Verificar que la mesa existe y obtener su circuito
        cursor.execute("""
            SELECT m.num, m.id_circuito, m.id_eleccion
            FROM mesa m 
            WHERE m.num = %s AND m.id_eleccion = %s
        """, (num_mesa, id_eleccion))
        
        mesa_info = cursor.fetchone()
        print(f"Mesa encontrada: {mesa_info}")
        
        if not mesa_info:
            return jsonify({"error": f"Mesa {num_mesa} no encontrada para la elección {id_eleccion}"}), 404

        id_circuito = mesa_info['id_circuito']

        # Verificar el tipo de elección
        cursor.execute("""SELECT id_tipo_eleccion
                       FROM eleccion 
                       WHERE id = %s
                       """, (id_eleccion,))
        
        eleccion = cursor.fetchone()
        print(f"Elección encontrada: {eleccion}")
        
        if not eleccion:
            return jsonify({"error": "Elección no encontrada"}), 404
            
        tipo_eleccion = eleccion['id_tipo_eleccion']
        print(f"Tipo de elección: {tipo_eleccion}")

        # Verificar si hay votos para este circuito y elección
        cursor.execute("""
            SELECT COUNT(*) as total_votos
            FROM voto v
            WHERE v.id_circuito = %s AND v.id_eleccion = %s
        """, (id_circuito, id_eleccion))
        
        total_votos_check = cursor.fetchone()
        print(f"Total votos en el circuito: {total_votos_check}")
        
        if total_votos_check['total_votos'] == 0:
            return jsonify([])  # Retornar array vacío en lugar de error
        
        if tipo_eleccion == 3:  # Plebiscito
            cursor.execute("""
                SELECT pp.valor, COUNT(*) AS total_votos
                FROM voto v
                JOIN voto_normal vn ON v.id = vn.id_voto
                JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
                JOIN papeleta_plebiscito pp ON vep.id_papeleta = pp.id_papeleta 
                    AND vep.id_eleccion = pp.id_eleccion
                WHERE v.id_circuito = %s AND v.id_eleccion = %s
                GROUP BY pp.valor
            """, (id_circuito, id_eleccion))
        else:  # Otras elecciones (con listas y partidos)
            cursor.execute("""
                SELECT l.id_papeleta as lista_id, p.nombre as partido, COUNT(*) AS total_votos
                FROM voto v
                JOIN voto_normal vn ON v.id = vn.id_voto
                JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
                JOIN lista l ON vep.id_papeleta = l.id_papeleta AND vep.id_eleccion = l.id_eleccion
                JOIN partido p ON l.id_partido = p.id
                WHERE v.id_circuito = %s AND v.id_eleccion = %s
                GROUP BY l.id_papeleta, p.nombre
            """, (id_circuito, id_eleccion))

        votos_normales = cursor.fetchall()
       
        
        return jsonify(votos_normales)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()