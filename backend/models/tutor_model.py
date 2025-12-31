import psycopg2
from config import Config

def get_conn():
    return psycopg2.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        port=Config.DB_PORT
    )


# ============================================================
#   1. OBTENER LISTA DE ESTUDIANTES DEL TUTOR
# ============================================================
def obtener_estudiantes_del_tutor(id_usuario_tutor):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT 
            a.id_alumno,
            u.nombre,
            u.apellido,
            u.email,
            a.codigo_estudiante,
            a.programa_estudio,
            a.semestre_actual
        FROM tutor t
        JOIN alumno a ON a.id_tutor = t.id_tutor
        JOIN usuarios u ON u.id_usuario = a.id_usuario
        WHERE t.id_usuario = %s;
    """

    cur.execute(sql, (id_usuario_tutor,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id_alumno": r[0],
            "nombre": r[1],
            "apellido": r[2],
            "email": r[3],
            "codigo_estudiante": r[4],
            "programa": r[5],
            "semestre": r[6]
        }
        for r in rows
    ]


# ============================================================
#   2. REGISTRAR UNA TUTORÍA
# ============================================================
def registrar_tutoria(data):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO registro_tutoria 
            (id_tutor, id_alumno, fecha_tutoria, tipo_tutoria, observaciones, derivaciones, id_cronograma)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    try:
        cur.execute(sql, (
            data["id_tutor"],
            data["id_alumno"],
            data["fecha_tutoria"],
            data["tipo_tutoria"],
            data["observaciones"],
            data.get("derivaciones", None),
            data.get("id_cronograma", None)
        ))

        conn.commit()
        return True

    except Exception as e:
        print("Error al registrar tutoría:", e)
        return False

    finally:
        cur.close()
        conn.close()


# ============================================================
#   3. OBTENER PRÓXIMAS TUTORÍAS DEL TUTOR
# ============================================================
def obtener_proximas_tutorias(id_usuario_tutor):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT 
            rt.id_registro,
            rt.fecha_tutoria,
            u.nombre AS alumno_nombre,
            u.apellido AS alumno_apellido,
            rt.tipo_tutoria
        FROM tutor t
        JOIN registro_tutoria rt ON rt.id_tutor = t.id_tutor
        JOIN alumno a ON a.id_alumno = rt.id_alumno
        JOIN usuarios u ON u.id_usuario = a.id_usuario
        WHERE t.id_usuario = %s
        ORDER BY rt.fecha_tutoria ASC;
    """

    cur.execute(sql, (id_usuario_tutor,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "fecha": r[1],
            "alumno": f"{r[2]} {r[3]}",
            "tipo": r[4]
        }
        for r in rows
    ]


# ============================================================
#   4. RETROALIMENTACIONES DEL TUTOR
# ============================================================
def obtener_retroalimentaciones(id_usuario_tutor):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT 
            r.id,
            r.comentario,
            r.fecha,
            u.nombre AS alumno_nombre,
            u.apellido AS alumno_apellido
        FROM retroalimentaciones r
        JOIN alumno a ON a.id_alumno = r.id_alumno
        JOIN usuarios u ON u.id_usuario = a.id_usuario
        JOIN tutor t ON t.id_tutor = r.id_tutor
        WHERE t.id_usuario = %s
        ORDER BY r.fecha DESC;
    """

    cur.execute(sql, (id_usuario_tutor,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "comentario": r[1],
            "fecha": r[2],
            "alumno": f"{r[3]} {r[4]}"
        }
        for r in rows
    ]


# ============================================================
#   5. CRONOGRAMAS DISPONIBLES
# ============================================================
def obtener_cronogramas_tutor():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            id_cronograma, semestre, ambiente, fecha_inicio, fecha_fin, estado
        FROM cronograma
        ORDER BY fecha_inicio DESC;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "semestre": r[1],
            "ambiente": r[2],
            "inicio": r[3],
            "fin": r[4],
            "estado": r[5]
        }
        for r in rows
    ]


# ============================================================
#   6. MATERIAS ASIGNADAS AL TUTOR
# ============================================================
def obtener_materias_del_tutor(id_usuario_tutor):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT 
            m.id_materia,
            m.nombre_materia,
            m.codigo_materia
        FROM tutor t
        JOIN tutor_materia tm ON tm.id_tutor = t.id_tutor
        JOIN materia m ON m.id_materia = tm.id_materia
        WHERE t.id_usuario = %s;
    """

    cur.execute(sql, (id_usuario_tutor,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id_materia": r[0],
            "nombre": r[1],
            "codigo": r[2]
        }
        for r in rows
    ]
