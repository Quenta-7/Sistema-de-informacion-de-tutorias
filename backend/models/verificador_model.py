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

# 1. TUTORIAS POR FECHA
def tutorias_por_fecha(fecha):
    conn = get_conn()
    cur = conn.cursor()
    # Usamos "cronograma" e "id_cronograma" según tu BD real
    sql = """
        SELECT 
            rt.fecha_tutoria, rt.tipo_tutoria, rt.observaciones, 
            u_alu.nombre, u_alu.apellido, u_tut.nombre
        FROM registro_tutoria rt
        JOIN alumno a ON rt.id_alumno = a.id_alumno
        JOIN usuarios u_alu ON a.id_usuario = u_alu.id_usuario
        JOIN tutor t ON rt.id_tutor = t.id_tutor
        JOIN usuarios u_tut ON t.id_usuario = u_tut.id_usuario
        WHERE DATE(rt.fecha_tutoria) = %s;
    """
    try:
        cur.execute(sql, (fecha,))
        rows = cur.fetchall()
        return [{"fecha": r[0].isoformat(), "tipo": r[1], "obs": r[2], "alumno": f"{r[3]} {r[4]}", "tutor": r[5]} for r in rows]
    except Exception as e:
        print("Error en tutorias_por_fecha:", e)
        return []
    finally:
        cur.close()
        conn.close()

# 2. TUTORIAS POR SEMESTRE (Aquí estaba el error del nombre de tabla)
def tutorias_por_semestre(semestre):
    conn = get_conn()
    cur = conn.cursor()
    # CORRECCIÓN: Cambiado "cronogramas" por "cronograma" 
    # y "id_cronos" por "id_cronograma"
    sql = """
        SELECT 
            rt.fecha_tutoria, rt.tipo_tutoria, u_alu.nombre, u_alu.apellido
        FROM registro_tutoria rt
        JOIN cronograma c ON rt.id_cronograma = c.id_cronograma
        JOIN alumno a ON rt.id_alumno = a.id_alumno
        JOIN usuarios u_alu ON a.id_usuario = u_alu.id_usuario
        WHERE c.semestre = %s;
    """
    try:
        cur.execute(sql, (semestre,))
        rows = cur.fetchall()
        return [{"fecha": r[0].isoformat(), "tipo": r[1], "alumno": f"{r[2]} {r[3]}"} for r in rows]
    except Exception as e:
        print("Error en tutorias_por_semestre:", e)
        return []
    finally:
        cur.close()
        conn.close()

# 3. SEGUIMIENTO POR ALUMNO
def seguimiento_por_alumno(id_usuario_alumno):
    conn = get_conn()
    cur = conn.cursor()
    sql = """
        SELECT 
            rt.fecha_tutoria, rt.tipo_tutoria, rt.observaciones, rt.derivaciones
        FROM registro_tutoria rt
        JOIN alumno a ON rt.id_alumno = a.id_alumno
        WHERE a.id_usuario = %s
        ORDER BY rt.fecha_tutoria DESC;
    """
    try:
        cur.execute(sql, (id_usuario_alumno,))
        rows = cur.fetchall()
        return [{"fecha": r[0].isoformat(), "tipo": r[1], "observaciones": r[2], "derivaciones": r[3]} for r in rows]
    except Exception as e:
        print("Error en seguimiento_por_alumno:", e)
        return []
    finally:
        cur.close()
        conn.close()