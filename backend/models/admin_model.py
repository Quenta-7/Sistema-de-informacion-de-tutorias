import psycopg2
import bcrypt
from config import Config


# ====================================================
#  CONEXIÓN A LA BASE DE DATOS
# ====================================================
def get_connection():
    return psycopg2.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        port=Config.DB_PORT
    )


# ====================================================
#  RESUMEN PARA EL DASHBOARD
# ====================================================
def obtener_resumen():
    conn = get_connection()
    cur = conn.cursor()

    consultas = {
        "estudiantes": "SELECT COUNT(*) FROM usuarios WHERE id_rol = 3;", # Cuenta a todos los usuarios alumnos
        "tutores": "SELECT COUNT(*) FROM usuarios WHERE id_rol = 2;",
        "cronogramas": "SELECT COUNT(*) FROM cronograma;",
        "tutorias": "SELECT COUNT(*) FROM registro_tutoria;"
    }

    resultado = {}

    for clave, sql in consultas.items():
        cur.execute(sql)
        resultado[clave] = cur.fetchone()[0]

    cur.close()
    conn.close()
    return resultado

def listar_usuarios_por_rol_paginado(id_rol, page=1, page_size=10):
    conn = get_connection()
    cur = conn.cursor()

    try:
        offset = (page - 1) * page_size

        cur.execute(
            """
            SELECT * FROM sp_listar_usuarios_por_rol_paginado(%s, %s, %s);
            """,
            (id_rol, page_size, offset)
        )

        rows = cur.fetchall()

        if not rows:
            return {
                "total": 0,
                "page": page,
                "page_size": page_size,
                "usuarios": []
            }

        total = rows[0][6]  # total_registros

        usuarios = [
            {
                "id_usuario": r[0],
                "nombre": r[1],
                "apellido": r[2],
                "email": r[3],
                "nombre_rol": r[4],
                "rol": r[5],
            }
            for r in rows
        ]

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "usuarios": usuarios
        }

    finally:
        cur.close()
        conn.close()

# ====================================================
#  LISTAR USUARIOS
# ====================================================
def listar_usuarios():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM sp_listar_usuarios();")
        rows = cur.fetchall()

        usuarios = [
            {
                "id_usuario": r[0],
                "nombre": r[1],
                "apellido": r[2],
                "email": r[3],
                "nombre_rol": r[4],
                "rol": r[5],
            }
            for r in rows
        ]

        return usuarios

    finally:
        cur.close()
        conn.close()

# ====================================================
#  CREAR USUARIOS
# ====================================================

def crear_usuario(nombre, apellido, email, password, id_rol):
    conn = get_connection()
    cur = conn.cursor()

    try:
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # 1. Crear usuario base
        sql_usuario = """
            SELECT sp_crear_usuario(%s, %s, %s, %s, %s);
        """
        cur.execute(sql_usuario, (
            nombre,
            apellido,
            email,
            password_hash,
            id_rol
        ))

        nuevo_id = cur.fetchone()[0]

        # 2. Crear registro según rol
        sql_rol = "CALL sp_crear_usuario_por_rol(%s, %s);"
        cur.execute(sql_rol, (nuevo_id, id_rol))

        conn.commit()
        return nuevo_id

    except Exception as e:
        conn.rollback()
        print(f"Error al crear usuario completo: {e}")
        raise e

    finally:
        cur.close()
        conn.close()


# ====================================================
#  TUTORES DISPONIBLES
# ====================================================
def tutores_disponibles():
    conn = get_connection()
    cur = conn.cursor()

    try:
        sql = "SELECT * FROM sp_tutores_disponibles();"
        cur.execute(sql)
        rows = cur.fetchall()

        tutores = [
            {
                "id_tutor": r[0],
                "nombre": r[1],
                "apellido": r[2],
                "codigo_docente": r[3],
            }
            for r in rows
        ]

        return tutores

    finally:
        cur.close()
        conn.close()

# ====================================================
#  ALUMNOS DISPONIBLES
# ====================================================

def alumnos_disponibles():
    conn = get_connection()
    cur = conn.cursor()

    try:
        sql = "SELECT * FROM sp_alumnos_disponibles();"
        cur.execute(sql)
        rows = cur.fetchall()

        alumnos = [
            {
                "id_alumno": r[0],
                "nombre": r[1],
                "apellido": r[2],
                "codigo_estudiante": r[3],
            }
            for r in rows
        ]

        return alumnos

    finally:
        cur.close()
        conn.close()



# ====================================================
#  LISTAR MATERIAS (PARA EL COMBO EN EL MODAL)
# ====================================================
def listar_materias():
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        SELECT id_materia, nombre_materia, codigo_materia
        FROM materia
        ORDER BY nombre_materia;
    """

    cur.execute(sql)
    rows = cur.fetchall()

    materias = [
        {
            "id_materia": r[0],
            "nombre_materia": r[1],
            "codigo_materia": r[2],
        }
        for r in rows
    ]

    cur.close()
    conn.close()
    return materias


# ====================================================
#  ASIGNAR TUTOR A UN ALUMNO
# ====================================================
def asignar_tutor(id_alumno, id_tutor, id_materia):
    """
    Crea una SOLICITUD + un REGISTRO_TUTORIA inicial.
    IMPORTANTE: id_materia NO puede ser NULL porque la columna
    en la tabla 'solicitud' es NOT NULL.
    """
    conn = get_connection()
    cur = conn.cursor()

    # 1) Crear solicitud
    cur.execute(
        """
        INSERT INTO solicitud
            (id_alumno, id_materia, fecha_solicitud, tema_especifico, estado_solicitud)
        VALUES
            (%s, %s, NOW(), 'Asignación de tutor', 'Asignado');
        """,
        (id_alumno, id_materia),
    )

    # 2) Crear primer registro de tutoría
    cur.execute(
        """
        INSERT INTO registro_tutoria
            (id_tutor, id_alumno, fecha_tutoria, tipo_tutoria,
             observaciones, derivaciones, id_cronograma)
        VALUES
            (%s, %s, NOW(), 'Asignación Inicial',
             'Asignado por administrador', NULL, NULL);
        """,
        (id_tutor, id_alumno),
    )

    conn.commit()
    cur.close()
    conn.close()
    return True
