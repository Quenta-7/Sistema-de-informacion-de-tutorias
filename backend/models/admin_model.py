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
        "estudiantes": "SELECT COUNT(*) FROM alumno;",
        "tutores": "SELECT COUNT(*) FROM tutor;",
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


# ====================================================
#  LISTAR USUARIOS
# ====================================================
def listar_usuarios():
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        SELECT u.id_usuario,
               u.nombre,
               u.apellido,
               u.email,
               r.nombre_rol,
               u.id_rol
        FROM usuarios u
        JOIN rol r ON r.id_rol = u.id_rol
        ORDER BY u.id_usuario;
    """

    cur.execute(sql)
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

    cur.close()
    conn.close()
    return usuarios


# ====================================================
#  CREAR USUARIO (ADMIN CREA NUEVOS USUARIOS)
# ====================================================
def crear_usuario(nombre, apellido, email, password, id_rol):
    """
    Crea un registro en la tabla USUARIOS.
    Devuelve el id_usuario recién creado.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Hash correcto con bcrypt (texto, no bytea en la BD)
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    sql = """
        INSERT INTO usuarios
            (nombre, apellido, email, password_hash, id_rol, telefono, fecha_registro)
        VALUES
            (%s, %s, %s, %s, %s, NULL, NOW())
        RETURNING id_usuario;
    """

    cur.execute(sql, (nombre, apellido, email, password_hash, id_rol))
    nuevo_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return nuevo_id


# ====================================================
#  TUTORES DISPONIBLES
# ====================================================
def tutores_disponibles():
    """
    Devuelve todos los tutores con su nombre y código.
    Se asume que TUTOR tiene fk hacia USUARIOS:
    - tutor.id_usuario -> usuarios.id_usuario
    """
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        SELECT
            t.id_tutor,
            u.nombre,
            u.apellido,
            t.codigo_docente
        FROM tutor t
        JOIN usuarios u ON u.id_usuario = t.id_usuario
        ORDER BY u.nombre;
    """

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

    cur.close()
    conn.close()
    return tutores


# ====================================================
#  ALUMNOS SIN TUTOR ASIGNADO
# ====================================================
def alumnos_disponibles():
    """
    Alumnos que NO tienen todavía solicitud de tutoría (no están asignados).
    Se asume:
    - alumno.id_usuario -> usuarios.id_usuario
    - solicitud.id_alumno referencia alumno.id_alumno
    """
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        SELECT
            a.id_alumno,
            u.nombre,
            u.apellido,
            a.codigo_estudiante
        FROM alumno a
        JOIN usuarios u ON u.id_usuario = a.id_usuario
        WHERE NOT EXISTS (
            SELECT 1
            FROM solicitud s
            WHERE s.id_alumno = a.id_alumno
        )
        ORDER BY u.nombre;
    """

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

    cur.close()
    conn.close()
    return alumnos


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
