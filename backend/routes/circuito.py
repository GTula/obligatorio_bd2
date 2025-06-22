from flask import Blueprint, jsonify, request
from db import get_db_connection

circuito_bp = Blueprint("circuito", __name__)

@circuito_bp.route("/", methods=["POST"])
def get_circuito_por_credencial():
    data = request.get_json()
    serie = data.get("serie")
    numero = data.get("numero")
    fecha = data.get("fecha")
    print(f"Parámetros recibidos: serie={serie}, numero={numero}, fecha={fecha}")

    if not (serie and numero and fecha):
        return jsonify({"error": "Faltan parámetros: serie, numero o fecha"}), 400

    conn = get_db_connection()
    try:
        cursor1 = conn.cursor(dictionary=True, buffered=True)  # Usar buffered para evitar problemas de conexión
        cursor1.execute("SELECT id FROM eleccion WHERE fecha = %s;", (fecha,))
        eleccion = cursor1.fetchone()
        if not eleccion:
            return jsonify({"error": "No se encontró una elección para esa fecha"}), 404
        cursor1.close()
        id_eleccion = eleccion["id"]
        print(f"id de elección encontrado: {id_eleccion}")

        cursor2 = conn.cursor(dictionary=True, buffered=True)  # Usar buffered para evitar problemas de conexión
        cursor2.execute("""
            SELECT a.id_circuito, a.id_eleccion
            FROM asignado a
            WHERE a.serie_credencial = %s AND a.numero_credencial = %s AND a.id_eleccion = %s;
        """, (serie, numero, id_eleccion))
        circuito = cursor2.fetchone()
        cursor2.close()

        if circuito:
            return jsonify(circuito)
        return jsonify({"error": "No se encontró circuito para esa credencial y elección"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@circuito_bp.route("/por-mesa", methods=["GET"])
def get_circuito_por_mesa():
    num_mesa = request.args.get("num_mesa")
    fecha = request.args.get("fecha")
    if not (num_mesa and fecha):
        return jsonify({"error": "Faltan parámetros: num_mesa o fecha"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        # Buscar el id de la elección por fecha
        cursor.execute("SELECT id FROM eleccion WHERE fecha = %s;", (fecha,))
        eleccion = cursor.fetchone()
        if not eleccion:
            return jsonify({"error": "No se encontró una elección para esa fecha"}), 404

        id_eleccion = eleccion["id"]

        cursor.execute("""
            SELECT id_circuito, id_eleccion
            FROM mesa
            WHERE num = %s AND id_eleccion = %s
        """, (num_mesa, id_eleccion))
        mesa = cursor.fetchone()
        if mesa:
            return jsonify({"id_circuito": mesa["id_circuito"], "id_eleccion": id_eleccion})
        return jsonify({"error": "No se encontró circuito para esa mesa y elección"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@circuito_bp.route("/votantes-circuito", methods=["GET"])
def get_votantes_circuito():
    id_circuito = request.args.get("id_circuito")
    id_eleccion = request.args.get("id_eleccion")
    
    if not (id_circuito and id_eleccion):
        return jsonify({"error": "Faltan parámetros: id_circuito o id_eleccion"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute("""
            SELECT c.nombre, c.apellido, cr.ci_ciudadano as ci, a.serie_credencial as serie, a.numero_credencial as numero
            FROM asignado a
            JOIN credencial cr ON a.serie_credencial = cr.serie AND a.numero_credencial = cr.numero
            JOIN ciudadano c ON cr.ci_ciudadano = c.ci
            WHERE a.id_circuito = %s AND a.id_eleccion = %s
            ORDER BY c.apellido, c.nombre;
        """, (id_circuito, id_eleccion))
        
        votantes = cursor.fetchall()
        return jsonify(votantes)
    except Exception as e:
        print("ERROR EN VOTANTES-ciRCUITO:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@circuito_bp.route("/resultados-circuito-lista", methods=["GET"])
def resultados_circuito_lista():
    id_circuito = request.args.get("id_circuito")
    id_eleccion = request.args.get("id_eleccion")
    if not (id_circuito and id_eleccion):
        return jsonify({"error": "Faltan parámetros: id_circuito o id_eleccion"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        # votos normales por partido/papeleta (no observados)
        cursor.execute("""
            SELECT
                l.id_papeleta AS id_lista,
                par.id AS id_partido,
                par.nombre AS nombre_partido,
                COUNT(*) AS cantidad_votos
            FROM voto_normal vn
            JOIN voto v ON vn.id_voto = v.id
            JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
            JOIN papeleta p ON vep.id_papeleta = p.id AND v.id_eleccion = p.id_eleccion
            JOIN lista l ON p.id = l.id_papeleta
            JOIN partido par ON l.id_partido = par.id
            WHERE
                v.id_circuito = %s
                AND v.id_eleccion = %s
                AND (vn.observado IS NULL OR vn.observado = 0)
            GROUP BY l.id_papeleta, par.id, par.nombre
            ORDER BY cantidad_votos DESC;
            """, (id_circuito, id_eleccion))
        votos_normales = cursor.fetchall()

        # votos normales observados por partido/papeleta
        cursor.execute("""
            SELECT
                l.id_papeleta AS id_lista,
                par.id AS id_partido,
                par.nombre AS nombre_partido,
                COUNT(*) AS cantidad_votos
            FROM voto_normal vn
            JOIN voto v ON vn.id_voto = v.id
            JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
            JOIN papeleta p ON vep.id_papeleta = p.id AND v.id_eleccion = p.id_eleccion
            JOIN lista l ON p.id = l.id_papeleta
            JOIN partido par ON l.id_partido = par.id
            WHERE
                v.id_circuito = %s
                AND v.id_eleccion = %s
                AND (vn.observado IS NULL OR vn.observado = 1)
            GROUP BY l.id_papeleta, par.id, par.nombre
            ORDER BY cantidad_votos DESC;
        """, (id_circuito, id_eleccion))
        votos_observados = cursor.fetchall()

        # votos anulados
        cursor.execute("""
            SELECT COUNT(*) as cantidad
            FROM voto_anulado va
            JOIN voto v ON va.id_voto = v.id
            WHERE v.id_circuito = %s AND v.id_eleccion = %s
        """, (id_circuito, id_eleccion))
        votos_anulados = cursor.fetchone()["cantidad"]

        # votos en blanco
        cursor.execute("""
            SELECT COUNT(*) as cantidad
            FROM voto_blanco vb
            JOIN voto v ON vb.id_voto = v.id
            WHERE v.id_circuito = %s AND v.id_eleccion = %s
        """, (id_circuito, id_eleccion))
        votos_blanco = cursor.fetchone()["cantidad"]

        return jsonify({
            "votos_normales": votos_normales,
            "votos_observados": votos_observados,
            "votos_anulados": votos_anulados,
            "votos_blanco": votos_blanco
        })
    except Exception as e:
        print("ERROR EN RESULTADOS-ciRCUITO:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@circuito_bp.route("/resultados-circuito-partido", methods=["GET"])
def resultados_circuito_partido():
    id_circuito = request.args.get("id_circuito")
    id_eleccion = request.args.get("id_eleccion")
    if not (id_circuito and id_eleccion):
        return jsonify({"error": "Faltan parámetros: id_circuito o id_eleccion"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        # votos normales por partido/papeleta (no observados)
        cursor.execute("""
            SELECT
                par.id AS id_partido,
                par.nombre AS nombre_partido,
                COUNT(*) AS cantidad_votos
            FROM voto_normal vn
            JOIN voto v ON vn.id_voto = v.id
            JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
            JOIN papeleta p ON vep.id_papeleta = p.id AND v.id_eleccion = p.id_eleccion
            JOIN lista l ON p.id = l.id_papeleta
            JOIN partido par ON l.id_partido = par.id
            WHERE
                v.id_circuito = %s
                AND v.id_eleccion = %s
                AND (vn.observado IS NULL OR vn.observado = 0)
            GROUP BY par.id, par.nombre
            ORDER BY cantidad_votos DESC;
            """, (id_circuito, id_eleccion))
        votos_normales = cursor.fetchall()

        # votos normales observados por partido/papeleta
        cursor.execute("""
            SELECT
                par.id AS id_partido,
                par.nombre AS nombre_partido,
                COUNT(*) AS cantidad_votos
            FROM voto_normal vn
            JOIN voto v ON vn.id_voto = v.id
            JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
            JOIN papeleta p ON vep.id_papeleta = p.id AND v.id_eleccion = p.id_eleccion
            JOIN lista l ON p.id = l.id_papeleta
            JOIN partido par ON l.id_partido = par.id
            WHERE
                v.id_circuito = %s
                AND v.id_eleccion = %s
                AND (vn.observado IS NULL OR vn.observado = 1)
            GROUP BY par.id, par.nombre
            ORDER BY cantidad_votos DESC;
        """, (id_circuito, id_eleccion))
        votos_observados = cursor.fetchall()

        # votos anulados
        cursor.execute("""
            SELECT COUNT(*) as cantidad
            FROM voto_anulado va
            JOIN voto v ON va.id_voto = v.id
            WHERE v.id_circuito = %s AND v.id_eleccion = %s
        """, (id_circuito, id_eleccion))
        votos_anulados = cursor.fetchone()["cantidad"]

        # votos en blanco
        cursor.execute("""
            SELECT COUNT(*) as cantidad
            FROM voto_blanco vb
            JOIN voto v ON vb.id_voto = v.id
            WHERE v.id_circuito = %s AND v.id_eleccion = %s
        """, (id_circuito, id_eleccion))
        votos_blanco = cursor.fetchone()["cantidad"]

        return jsonify({
            "votos_normales": votos_normales,
            "votos_observados": votos_observados,
            "votos_anulados": votos_anulados,
            "votos_blanco": votos_blanco
        })
    except Exception as e:
        print("ERROR EN RESULTADOS-ciRCUITO:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@circuito_bp.route("/resultados-circuito-plebiscito", methods=["GET"])
def resultados_circuito_plebiscito():
    id_circuito = request.args.get("id_circuito")
    id_eleccion = request.args.get("id_eleccion")
    if not (id_circuito and id_eleccion):
        return jsonify({"error": "Faltan parámetros: id_circuito o id_eleccion"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    try:
        # votos por opción en el plebiscito
        cursor.execute("""
            SELECT
                pp.id_papeleta AS id_opcion,
                pp.nombre AS nombre_opcion,
                pp.valor AS valor_opcion,
                COUNT(*) AS cantidad_votos
            FROM voto_normal vn
            JOIN voto v ON vn.id_voto = v.id
            JOIN voto_elige_papeleta vep ON vn.id_voto = vep.id_voto_normal
            JOIN papeleta p ON vep.id_papeleta = p.id AND v.id_eleccion = p.id_eleccion
            JOIN papeleta_plebiscito pp ON p.id = pp.id_papeleta AND p.id_eleccion = pp.id_eleccion
            WHERE v.id_circuito = %s AND v.id_eleccion = %s
            GROUP BY pp.id_papeleta, pp.nombre
            ORDER BY cantidad_votos DESC;
        """, (id_circuito, id_eleccion))
        votos_plebiscito = cursor.fetchall()

        # votos anulados
        cursor.execute("""
            SELECT COUNT(*) as cantidad
            FROM voto_anulado va
            JOIN voto v ON va.id_voto = v.id
            WHERE v.id_circuito = %s AND v.id_eleccion = %s
        """, (id_circuito, id_eleccion))
        votos_anulados = cursor.fetchone()["cantidad"]

        # votos en blanco
        cursor.execute("""
            SELECT COUNT(*) as cantidad
            FROM voto_blanco vb
            JOIN voto v ON vb.id_voto = v.id
            WHERE v.id_circuito = %s AND v.id_eleccion = %s
        """, (id_circuito, id_eleccion))
        votos_blanco = cursor.fetchone()["cantidad"]

        return jsonify({
            "votos_plebiscito": votos_plebiscito,
            "votos_anulados": votos_anulados,
            "votos_blanco": votos_blanco
        })
    except Exception as e:
        print("ERROR EN RESULTADOS-CIRCUITO:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()