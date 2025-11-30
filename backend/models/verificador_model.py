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

# ==========================
#   OBTENER TUTOR
# ==========================
def obtener_tutor(id_usuario):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT 
            u.nombre,
            u.apellido,
            t.codigo_docente,
            t.departamento
        FROM alumno a
        JOIN tutor t ON t.id_tutor = a.id_tutor
        JOIN usuarios u ON u.id_usuario = t.id_usuario
        WHERE a.id_usuario = %s;
    """

    cur.execute(sql, (id_usuario,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "nombre": row[0],
        "apellido": row[1],
        "codigo_docente": row[2],
        "departamento": row[3]
    }


# ==========================
#   HORARIO DE TUTORÍAS
# ==========================
def obtener_horario(id_usuario):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT 
            c.semestre,
            c.ambiente,
            c.fecha_inicio,
            c.fecha_fin,
            c.estado
        FROM alumno a
        JOIN registro_tutoria rt ON rt.id_alumno = a.id_alumno
        JOIN cronograma c ON c.id_cronograma = rt.id_cronograma
        WHERE a.id_usuario = %s;
    """

    cur.execute(sql, (id_usuario,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "semestre": r[0],
            "ambiente": r[1],
            "inicio": r[2],
            "fin": r[3],
            "estado": r[4]
        }
        for r in rows
    ]


# ==========================
#   RETROALIMENTACIONES
# ==========================
def obtener_feedback(id_usuario):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT 
            r.comentario,
            r.fecha,
            u.nombre,
            u.apellido
        FROM retroalimentaciones r
        JOIN alumno a ON a.id_alumno = r.id_alumno
        JOIN usuarios u ON u.id_usuario = r.id_tutor
        WHERE a.id_usuario = %s;
    """

    cur.execute(sql, (id_usuario,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "comentario": r[0],
            "fecha": r[1],
            "tutor_nombre": r[2],
            "tutor_apellido": r[3]
        }
        for r in rows
    ]
