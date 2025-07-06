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
        
        if not mesa_info:
            return jsonify({"error": f"Mesa {num_mesa} no encontrada para la elección {id_eleccion}"}), 404

        id_circuito = mesa_info['id_circuito']

        # Verificar el tipo de elección
        cursor.execute("""SELECT id_tipo_eleccion FROM eleccion WHERE id = %s""", (id_eleccion,))
        eleccion = cursor.fetchone()
        
        if not eleccion:
            return jsonify({"error": "Elección no encontrada"}), 404
            
        tipo_eleccion = eleccion['id_tipo_eleccion']

        # Obtener total de votos (todos los votos: normales + anulados + blancos)
        cursor.execute("""
            SELECT COUNT(*) as total_votos
            FROM voto v
            WHERE v.id_circuito = %s AND v.id_eleccion = %s
        """, (id_circuito, id_eleccion))
        
        total_votos_result = cursor.fetchone()
        total_votos = total_votos_result['total_votos'] if total_votos_result else 0
        
        # Obtener votos anulados
        cursor.execute("""
            SELECT COUNT(*) as total_votos
            FROM voto v
            JOIN voto_anulado va ON v.id = va.id_voto
            WHERE v.id_circuito = %s AND v.id_eleccion = %s
        """, (id_circuito, id_eleccion))
        
        votos_anulados = cursor.fetchone()['total_votos']
        
        # Obtener votos en blanco
        cursor.execute("""
            SELECT COUNT(*) as total_votos
            FROM voto v
            JOIN voto_blanco vb ON v.id = vb.id_voto
            WHERE v.id_circuito = %s AND v.id_eleccion = %s
        """, (id_circuito, id_eleccion))
        
        votos_blanco = cursor.fetchone()['total_votos']
        
        if total_votos == 0:
            return jsonify({
                "tipo_eleccion": tipo_eleccion,
                "total_votos": 0,
                "tabla_lista_partido": [],
                "tabla_partido": [],
                "tabla_partido_candidato": [],
                "tabla_ganadores_departamento": []
            })
        
        if tipo_eleccion == 3:  # Plebiscito
            cursor.execute("""
                SELECT pp.valor, COUNT(*) AS cant_votos
                FROM voto v
                JOIN voto_normal vn ON v.id = vn.id_voto
                JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
                JOIN papeleta_plebiscito pp ON vep.id_papeleta = pp.id_papeleta 
                    AND vep.id_eleccion = pp.id_eleccion
                WHERE v.id_circuito = %s AND v.id_eleccion = %s
                GROUP BY pp.valor
            """, (id_circuito, id_eleccion))
            
            votos_plebiscito = cursor.fetchall()
            
            # Agregar votos en blanco y anulados
            if votos_blanco > 0:
                votos_plebiscito.append({'valor': 'En Blanco', 'cant_votos': votos_blanco})
            if votos_anulados > 0:
                votos_plebiscito.append({'valor': 'Anulado', 'cant_votos': votos_anulados})
            
            # Calcular porcentajes
            for voto in votos_plebiscito:
                voto['porcentaje'] = round((voto['cant_votos'] / total_votos) * 100, 2)
            
            return jsonify({
                "tipo_eleccion": tipo_eleccion,
                "total_votos": total_votos,
                "votos_plebiscito": votos_plebiscito,
                "tabla_ganadores_departamento": []  # No aplica para plebiscitos
            })
        
        else:  # Otras elecciones (con listas y partidos)
            
            # TABLA 1: Lista - Partido - Cant. Votos - Porcentaje
            cursor.execute("""
                SELECT 
                    l.id_papeleta as lista_id,
                    p.nombre as partido,
                    COUNT(DISTINCT v.id) AS cant_votos
                FROM voto v
                JOIN voto_normal vn ON v.id = vn.id_voto
                JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
                JOIN lista l ON vep.id_papeleta = l.id_papeleta AND vep.id_eleccion = l.id_eleccion
                JOIN partido p ON l.id_partido = p.id
                WHERE v.id_circuito = %s AND v.id_eleccion = %s
                GROUP BY l.id_papeleta, p.nombre
                ORDER BY cant_votos DESC
            """, (id_circuito, id_eleccion))
            
            tabla_lista_partido = cursor.fetchall()
            
            # TABLA 2: Partido - Votos - Porcentaje (agrupado por partido)
            cursor.execute("""
                SELECT 
                    p.nombre as partido,
                    COUNT(DISTINCT v.id) AS cant_votos
                FROM voto v
                JOIN voto_normal vn ON v.id = vn.id_voto
                JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
                JOIN lista l ON vep.id_papeleta = l.id_papeleta AND vep.id_eleccion = l.id_eleccion
                JOIN partido p ON l.id_partido = p.id
                WHERE v.id_circuito = %s AND v.id_eleccion = %s
                GROUP BY p.id, p.nombre
                ORDER BY cant_votos DESC
            """, (id_circuito, id_eleccion))
            
            tabla_partido = cursor.fetchall()
            
            # TABLA 3: Partido - Candidato - Cant Votos - Porcentaje
            cursor.execute("""
                SELECT 
                    p.nombre as partido,
                    CONCAT(cd.nombre, ' ', cd.apellido) as candidato,
                    COUNT(DISTINCT v.id) AS cant_votos
                FROM voto v
                JOIN voto_normal vn ON v.id = vn.id_voto
                JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
                JOIN lista l ON vep.id_papeleta = l.id_papeleta AND vep.id_eleccion = l.id_eleccion
                JOIN partido p ON l.id_partido = p.id
                JOIN candidato_por_lista cp ON l.id_papeleta = cp.id_papeleta AND l.id_eleccion = cp.id_eleccion
                JOIN ciudadano cd ON cp.id_candidato = cd.ci
                WHERE v.id_circuito = %s AND v.id_eleccion = %s
                GROUP BY p.id, p.nombre, cd.ci, cd.nombre, cd.apellido, l.id_papeleta
                ORDER BY p.nombre, cant_votos DESC
            """, (id_circuito, id_eleccion))
            
            tabla_partido_candidato = cursor.fetchall()
            
            # NUEVA TABLA 4: Ganadores por Departamento
            cursor.execute("""
                WITH votos_por_departamento AS (
                    SELECT 
                        d.id as id_departamento,
                        d.nombre as departamento,
                        p.nombre as partido,
                        l.id_papeleta as lista_id,
                        COUNT(DISTINCT v.id) AS cant_votos,
                        ROW_NUMBER() OVER (PARTITION BY d.id ORDER BY COUNT(DISTINCT v.id) DESC) as ranking
                    FROM voto v
                    JOIN voto_normal vn ON v.id = vn.id_voto
                    JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
                    JOIN lista l ON vep.id_papeleta = l.id_papeleta AND vep.id_eleccion = l.id_eleccion
                    JOIN partido p ON l.id_partido = p.id
                    JOIN circuito c ON v.id_circuito = c.id AND v.id_eleccion = c.id_eleccion
                    JOIN establecimiento e ON c.id_establecimiento = e.id
                    JOIN zona z ON e.id_zona = z.id AND e.id_departamento = z.id_departamento
                    JOIN departamento d ON z.id_departamento = d.id
                    WHERE v.id_eleccion = %s
                        AND l.id_departamento = d.id  -- Solo listas del mismo departamento
                    GROUP BY d.id, d.nombre, p.id, p.nombre, l.id_papeleta
                ),
                total_votos_departamento AS (
                    SELECT 
                        d.id as id_departamento,
                        COUNT(DISTINCT v.id) AS total_votos_depto
                    FROM voto v
                    JOIN voto_normal vn ON v.id = vn.id_voto
                    JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
                    JOIN lista l ON vep.id_papeleta = l.id_papeleta AND vep.id_eleccion = l.id_eleccion
                    JOIN circuito c ON v.id_circuito = c.id AND v.id_eleccion = c.id_eleccion
                    JOIN establecimiento e ON c.id_establecimiento = e.id
                    JOIN zona z ON e.id_zona = z.id AND e.id_departamento = z.id_departamento
                    JOIN departamento d ON z.id_departamento = d.id
                    WHERE v.id_eleccion = %s
                        AND l.id_departamento = d.id
                    GROUP BY d.id
                )
                SELECT 
                    vpd.departamento,
                    vpd.partido as partido_ganador,
                    vpd.lista_id,
                    vpd.cant_votos,
                    tvd.total_votos_depto,
                    ROUND((vpd.cant_votos * 100.0 / tvd.total_votos_depto), 2) as porcentaje
                FROM votos_por_departamento vpd
                JOIN total_votos_departamento tvd ON vpd.id_departamento = tvd.id_departamento
                WHERE vpd.ranking = 1
                ORDER BY vpd.departamento
            """, (id_eleccion, id_eleccion))
            
            tabla_ganadores_departamento = cursor.fetchall()
            
            # Agregar votos en blanco y anulados a las tablas principales
            if votos_blanco > 0:
                tabla_lista_partido.append({
                    'lista_id': 'En Blanco',
                    'partido': 'En Blanco',
                    'cant_votos': votos_blanco
                })
                tabla_partido.append({
                    'partido': 'En Blanco',
                    'cant_votos': votos_blanco
                })
                tabla_partido_candidato.append({
                    'partido': 'En Blanco',
                    'candidato': 'En Blanco',
                    'cant_votos': votos_blanco
                })
            
            if votos_anulados > 0:
                tabla_lista_partido.append({
                    'lista_id': 'Anulado',
                    'partido': 'Anulado',
                    'cant_votos': votos_anulados
                })
                tabla_partido.append({
                    'partido': 'Anulado',
                    'cant_votos': votos_anulados
                })
                tabla_partido_candidato.append({
                    'partido': 'Anulado',
                    'candidato': 'Anulado',
                    'cant_votos': votos_anulados
                })
            
            # Calcular porcentajes para las tablas principales
            for item in tabla_lista_partido:
                item['porcentaje'] = round((item['cant_votos'] / total_votos) * 100, 2)
                
            for item in tabla_partido:
                item['porcentaje'] = round((item['cant_votos'] / total_votos) * 100, 2)
                
            for item in tabla_partido_candidato:
                item['porcentaje'] = round((item['cant_votos'] / total_votos) * 100, 2)
            
            return jsonify({
                "tipo_eleccion": tipo_eleccion,
                "total_votos": total_votos,
                "votos_normales": total_votos - votos_anulados - votos_blanco,
                "votos_anulados": votos_anulados,
                "votos_blanco": votos_blanco,
                "tabla_lista_partido": tabla_lista_partido,
                "tabla_partido": tabla_partido,
                "tabla_partido_candidato": tabla_partido_candidato,
                "tabla_ganadores_departamento": tabla_ganadores_departamento
            })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
