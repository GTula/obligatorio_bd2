from flask import Blueprint, jsonify, request
from db import get_db_connection

votantes_bp = Blueprint("votantes", __name__)

@votantes_bp.route('/circuito/<int:id_circuito>/eleccion/<int:id_eleccion>', methods=['GET'])
def get_votantes_habilitados(id_circuito, id_eleccion):
    """Obtener lista de votantes habilitados para un circuito y elección"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute("""
            SELECT 
                a.serie_credencial,
                a.numero_credencial,
                c.ci_ciudadano,
                ci.nombre,
                ci.apellido,
                ci.fecha_nac,
                CASE 
                    WHEN ve.serie_credencial IS NOT NULL THEN 1 
                    ELSE 0 
                END as ya_voto,
                ve.observado
            FROM asignado a
            JOIN credencial c ON a.serie_credencial = c.serie AND a.numero_credencial = c.numero
            JOIN ciudadano ci ON c.ci_ciudadano = ci.ci
            LEFT JOIN vota_en ve ON a.serie_credencial = ve.serie_credencial 
                AND a.numero_credencial = ve.numero_credencial
                AND a.id_circuito = ve.id_circuito 
                AND a.id_eleccion = ve.id_eleccion
            WHERE a.id_circuito = %s AND a.id_eleccion = %s
            ORDER BY ci.apellido, ci.nombre
        """, (id_circuito, id_eleccion))

        votantes = cursor.fetchall()
        
        # Estadísticas
        total_habilitados = len(votantes)
        total_votaron = sum(1 for v in votantes if v['ya_voto'])
        
        return jsonify({
            'votantes': votantes,
            'estadisticas': {
                'total_habilitados': total_habilitados,
                'total_votaron': total_votaron,
                'pendientes': total_habilitados - total_votaron
            }
        })
        
    except Exception as e:
        print(f"Error obteniendo votantes: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@votantes_bp.route('/buscar', methods=['GET'])
def buscar_votante():
    """Buscar votante por credencial"""
    serie = request.args.get('serie')
    numero = request.args.get('numero')
    id_circuito = request.args.get('id_circuito')
    id_eleccion = request.args.get('id_eleccion')
    
    if not all([serie, numero, id_circuito, id_eleccion]):
        return jsonify({"error": "Faltan parámetros requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute("""
            SELECT 
                a.serie_credencial,
                a.numero_credencial,
                c.ci_ciudadano,
                ci.nombre,
                ci.apellido,
                ci.fecha_nac,
                CASE 
                    WHEN ve.serie_credencial IS NOT NULL THEN 1 
                    ELSE 0 
                END as ya_voto,
                ve.observado
            FROM asignado a
            JOIN credencial c ON a.serie_credencial = c.serie AND a.numero_credencial = c.numero
            JOIN ciudadano ci ON c.ci_ciudadano = ci.ci
            LEFT JOIN vota_en ve ON a.serie_credencial = ve.serie_credencial 
                AND a.numero_credencial = ve.numero_credencial
                AND a.id_circuito = ve.id_circuito 
                AND a.id_eleccion = ve.id_eleccion
            WHERE a.serie_credencial = %s 
                AND a.numero_credencial = %s
                AND a.id_circuito = %s 
                AND a.id_eleccion = %s
        """, (serie, numero, id_circuito, id_eleccion))

        votante = cursor.fetchone()
        
        if not votante:
            return jsonify({"error": "Votante no encontrado o no habilitado para este circuito"}), 404
            
        return jsonify(votante)
        
    except Exception as e:
        print(f"Error buscando votante: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@votantes_bp.route('/marcar-voto', methods=['POST'])
def marcar_como_votado():
    """Marcar votante como que ya votó"""
    data = request.json
    
    required_fields = ['serie_credencial', 'numero_credencial', 'id_circuito', 'id_eleccion']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar que el votante esté habilitado
        cursor.execute("""
            SELECT 1 FROM asignado 
            WHERE serie_credencial = %s 
                AND numero_credencial = %s
                AND id_circuito = %s 
                AND id_eleccion = %s
        """, (data['serie_credencial'], data['numero_credencial'], 
              data['id_circuito'], data['id_eleccion']))
        
        if not cursor.fetchone():
            return jsonify({"error": "Votante no habilitado para este circuito"}), 400

        # Verificar que no haya votado ya
        cursor.execute("""
            SELECT 1 FROM vota_en 
            WHERE serie_credencial = %s 
                AND numero_credencial = %s
                AND id_circuito = %s 
                AND id_eleccion = %s
        """, (data['serie_credencial'], data['numero_credencial'], 
              data['id_circuito'], data['id_eleccion']))
        
        if cursor.fetchone():
            return jsonify({"error": "El votante ya fue marcado como votado"}), 400

        # Insertar en vota_en
        observado = data.get('observado', False)
        cursor.execute("""
            INSERT INTO vota_en (serie_credencial, numero_credencial, id_circuito, id_eleccion, observado)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['serie_credencial'], data['numero_credencial'], 
              data['id_circuito'], data['id_eleccion'], observado))

        # Crear registro de voto
        cursor.execute("""
            INSERT INTO voto (id_circuito, id_eleccion, observado)
            VALUES (%s, %s, %s)
        """, (data['id_circuito'], data['id_eleccion'], observado))
        
        voto_id = cursor.lastrowid
        
        conn.commit()
        
        return jsonify({
            "mensaje": "Votante marcado como votado exitosamente",
            "voto_id": voto_id
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error marcando voto: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@votantes_bp.route('/desmarcar-voto', methods=['POST'])
def desmarcar_votado():
    """Desmarcar votante (para correcciones)"""
    data = request.json
    
    required_fields = ['serie_credencial', 'numero_credencial', 'id_circuito', 'id_eleccion']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Eliminar de vota_en
        cursor.execute("""
            DELETE FROM vota_en 
            WHERE serie_credencial = %s 
                AND numero_credencial = %s
                AND id_circuito = %s 
                AND id_eleccion = %s
        """, (data['serie_credencial'], data['numero_credencial'], 
              data['id_circuito'], data['id_eleccion']))
        
        if cursor.rowcount == 0:
            return jsonify({"error": "No se encontró registro de voto para desmarcar"}), 404
        
        conn.commit()
        
        return jsonify({"mensaje": "Voto desmarcado exitosamente"})
        
    except Exception as e:
        conn.rollback()
        print(f"Error desmarcando voto: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
