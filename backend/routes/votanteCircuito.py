from flask import Blueprint, request, jsonify
import mysql.connector
from db import get_db_connection

votacion_bp = Blueprint('votacion', __name__)

# ---------- GET /opciones/<id_eleccion> ----------
@votacion_bp.route('/opciones/<int:id_eleccion>', methods=['GET'])
def obtener_opciones_voto(id_eleccion):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 1. Tipo de elección
        cursor.execute("""
            SELECT te.nombre AS tipo_eleccion
            FROM eleccion e
            JOIN tipo_eleccion te ON e.id_tipo_eleccion = te.id
            WHERE e.id = %s
        """, (id_eleccion,))
        eleccion = cursor.fetchone()

        if not eleccion:
            return jsonify({'error': 'Elección no encontrada'}), 404

        response = {
            'tipo_eleccion': eleccion['tipo_eleccion'],
            'listas': [],
            'plebiscito': None
        }

        # 2A. Elecciones con listas
        if eleccion['tipo_eleccion'] in ['Presidencial', 'Municipal', 'Departamental']:
            cursor.execute("""
                SELECT 
                    p.id AS id_partido,
                    p.nombre AS nombre_partido,
                    l.id_papeleta,
                    l.organo,
                    GROUP_CONCAT(CONCAT(c.ci_ciudadano, '|', ciu.nombre, ' ', ciu.apellido) SEPARATOR ';') AS candidatos
                FROM lista l
                JOIN partido p ON l.id_partido = p.id
                LEFT JOIN candidato_por_lista cpl ON l.id_papeleta = cpl.id_papeleta
                                              AND l.id_eleccion = cpl.id_eleccion
                LEFT JOIN candidato c ON cpl.id_candidato = c.ci_ciudadano
                LEFT JOIN ciudadano ciu ON c.ci_ciudadano = ciu.ci
                WHERE l.id_eleccion = %s
                GROUP BY l.id_papeleta
            """, (id_eleccion,))

            for lista in cursor.fetchall():
                candidatos = []
                if lista['candidatos']:
                    for cand in lista['candidatos'].split(';'):
                        ci, nombre = cand.split('|')
                        candidatos.append({'ci': int(ci), 'nombre_completo': nombre})

                response['listas'].append({
                    'id_papeleta': lista['id_papeleta'],
                    'partido': {
                        'id': lista['id_partido'],
                        'nombre': lista['nombre_partido']
                    },
                    'organo': lista['organo'],
                    'candidatos': candidatos
                })

        # 2B. Plebiscito
        elif eleccion['tipo_eleccion'] == 'Plebiscito':
            cursor.execute("""
                SELECT id_papeleta, nombre, valor
                FROM papeleta_plebiscito
                WHERE id_eleccion = %s
            """, (id_eleccion,))
            opciones = cursor.fetchall()
            if opciones:
                response['plebiscito'] = {
                    'nombre': opciones[0]['nombre'],
                    'opciones': [
                        {'id_papeleta': op['id_papeleta'], 'valor': op['valor']}
                        for op in opciones
                    ]
                }

        return jsonify(response)

    except mysql.connector.Error as err:
        return jsonify({'error': f'Error de base de datos: {err}'}), 500
    finally:
        cursor.close()
        conn.close()          # buena práctica

# ---------- POST /votar ----------
@votacion_bp.route('/votar', methods=['POST'])
def registrar_voto():
    data = request.get_json()
    ci_ciudadano   = data.get('ci')
    id_eleccion    = data.get('id_eleccion')
    tipo_voto      = data.get('tipo_voto')          # 'normal', 'blanco', 'anulado'
    id_papeleta    = data.get('id_papeleta')
    valor_plebiscito = data.get('valor_plebiscito')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        conn.start_transaction()

        # 1. Verificar si ya votó
        cursor.execute("""
            SELECT 1
            FROM vota_en ve
            JOIN credencial c ON ve.serie_credencial = c.serie
                              AND ve.numero_credencial = c.numero
            WHERE c.ci_ciudadano = %s AND ve.id_eleccion = %s
        """, (ci_ciudadano, id_eleccion))
        if cursor.fetchone():
            return jsonify({'error': 'El ciudadano ya votó en esta elección'}), 400

        # 2. Circuito asignado
        cursor.execute("""
            SELECT a.id_circuito
            FROM asignado a
            JOIN credencial c ON a.serie_credencial = c.serie
                              AND a.numero_credencial = c.numero
            WHERE c.ci_ciudadano = %s AND a.id_eleccion = %s
        """, (ci_ciudadano, id_eleccion))
        fila = cursor.fetchone()
        if not fila:
            return jsonify({'error': 'Ciudadano no asignado a circuito'}), 400
        id_circuito = fila[0]

        # 3. Insert en vota_en
        cursor.execute("""
            INSERT INTO vota_en (serie_credencial, numero_credencial, id_circuito, id_eleccion, observado)
            SELECT serie, numero, %s, %s, FALSE
            FROM credencial
            WHERE ci_ciudadano = %s
        """, (id_circuito, id_eleccion, ci_ciudadano))

        # 4. Insert voto
        cursor.execute("""
            INSERT INTO voto (id_circuito, id_eleccion, observado)
            VALUES (%s, %s, FALSE)
        """, (id_circuito, id_eleccion))
        id_voto = cursor.lastrowid

        # 5. Tipo de voto
        if tipo_voto == 'blanco':
            cursor.execute("INSERT INTO voto_blanco (id_voto) VALUES (%s)", (id_voto,))

        elif tipo_voto == 'anulado':
            cursor.execute("INSERT INTO voto_anulado (id_voto) VALUES (%s)", (id_voto,))

        elif tipo_voto == 'normal':
            cursor.execute("""
                INSERT INTO voto_normal (id_voto, observado)
                VALUES (%s, FALSE)
            """, (id_voto,))
            id_voto_normal = cursor.lastrowid

            # Plebiscito
            if valor_plebiscito:
                cursor.execute("""
                    SELECT id_papeleta
                    FROM papeleta_plebiscito
                    WHERE id_eleccion = %s AND valor = %s
                """, (id_eleccion, valor_plebiscito))
                papeleta = cursor.fetchone()
                if not papeleta:
                    raise ValueError('Opción de plebiscito inválida')
                id_papeleta = papeleta[0]

            cursor.execute("""
                INSERT INTO voto_elige_papeleta (id_voto_normal, id_papeleta, id_eleccion)
                VALUES (%s, %s, %s)
            """, (id_voto_normal, id_papeleta, id_eleccion))

        conn.commit()
        return jsonify({'mensaje': 'Voto registrado exitosamente'}), 200

    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': f'Error de base de datos: {err}'}), 500
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()
