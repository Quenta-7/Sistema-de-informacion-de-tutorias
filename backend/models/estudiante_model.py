import psycopg2
from config import Config


def get_connection():
    return psycopg2.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        port=Config.DB_PORT
    )


# ===========================================================
#   OBTENER TUTOR ASIGNADO
# ===========================================================
def obtener_tutor_asignado(id_usuario):
    try:
        conn = get_connection()
        cur = conn.cursor()

        sql = """
            SELECT 
                t.id_tutor,
                u2.nombre,
                u2.apellido,
                t.departamento
            FROM alumno a
            JOIN registro_tutoria rt ON rt.id_alumno = a.id_alumno
            JOIN tutor t ON t.id_tutor = rt.id_tutor
            JOIN usuarios u2 ON u2.id_usuario = t.id_usuario
            WHERE a.id_usuario = %s
            LIMIT 1;
        """

        cur.execute(sql, (id_usuario,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if not row:
            return None

        return {
            "id_tutor": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "departamento": row[3]
        }

    except Exception as e:
        print("ERROR obtener_tutor_asignado:", e)
        return None


# ===========================================================
#   OBTENER HORARIO DEL ESTUDIANTE
# ===========================================================
def obtener_horario_estudiante(id_usuario):
    try:
        conn = get_connection()
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

        horarios = []
        for r in rows:
            horarios.append({
                "semestre": r[0],
                "ambiente": r[1],
                "fecha_inicio": r[2],
                "fecha_fin": r[3],
                "estado": r[4]
            })

        return horarios

    except Exception as e:
        print("ERROR obtener_horario_estudiante:", e)
        return []


# ===========================================================
#   OBTENER RETROALIMENTACIONES
# ===========================================================
def obtener_retroalimentaciones(id_usuario):
    try:
        conn = get_connection()
        cur = conn.cursor()

        sql = """
            SELECT r.comentario, r.fecha
            FROM alumno a
            JOIN retroalimentaciones r ON r.id_alumno = a.id_alumno
            WHERE a.id_usuario = %s;
        """

        cur.execute(sql, (id_usuario,))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        retro = []
        for r in rows:
            retro.append({
                "comentario": r[0],
                "fecha": r[1]
            })

        return retro

    except Exception as e:
        print("ERROR obtener_retroalimentaciones:", e)
        return []
