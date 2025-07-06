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
@votacion_bp.route('/emitir_voto', methods=['POST'])
def emitir_voto_simple():
    data = request.get_json()
    id_eleccion = data.get('id_eleccion')
    tipo_voto = data.get('tipo_voto')  # 'normal', 'blanco', 'anulado'
    id_papeleta = data.get('id_papeleta')
    valor_plebiscito = data.get('valor_plebiscito')
    id_circuito = data.get('id_circuito')  # 🧠 este parámetro se necesita sí o sí

    if not id_eleccion or not tipo_voto or not id_circuito:
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        conn.start_transaction()

        # 1. Insert en voto
        cursor.execute("""
            INSERT INTO voto (id_circuito, id_eleccion, observado)
            VALUES (%s, %s, FALSE)
        """, (id_circuito, id_eleccion))
        id_voto = cursor.lastrowid

        # 2. Según el tipo de voto
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

            if not id_papeleta:
                return jsonify({'error': 'Falta id_papeleta para voto normal'}), 400

            cursor.execute("""
                INSERT INTO voto_elige_papeleta (id_voto_normal, id_papeleta, id_eleccion)
                VALUES (%s, %s, %s)
            """, (id_voto_normal, id_papeleta, id_eleccion))

        else:
            return jsonify({'error': 'Tipo de voto inválido'}), 400

        conn.commit()
        return jsonify({'mensaje': 'Voto registrado'}), 200

    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': f'Error de base de datos: {err}'}), 500
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

