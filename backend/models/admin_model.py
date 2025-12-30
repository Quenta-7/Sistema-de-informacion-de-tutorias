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
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Encriptar contraseña
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # 1. Insertar en la tabla principal de usuarios
        sql_user = """
            INSERT INTO usuarios (nombre, apellido, email, password_hash, id_rol, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING id_usuario;
        """
        cur.execute(sql_user, (nombre, apellido, email, password_hash, id_rol))
        nuevo_id = cur.fetchone()[0]

        # 2. Insertar en tablas específicas según el Rol
        if id_rol == 2:  # TUTOR
            sql_tutor = """
                INSERT INTO tutor (id_usuario, codigo_docente, departamento_academico)
                VALUES (%s, %s, %s);
            """
            # Usamos valores genéricos que luego el admin puede editar
            cur.execute(sql_tutor, (nuevo_id, f"DOC-{nuevo_id}", "Sistemas"))

        elif id_rol == 3:  # ALUMNO
            sql_alumno = """
                INSERT INTO alumno (id_usuario, codigo_estudiante, programa_estudio, semestre_actual)
                VALUES (%s, %s, %s, %s);
            """
            cur.execute(sql_alumno, (nuevo_id, f"EST-{nuevo_id}", "Ing. Informática", "1"))

        elif id_rol == 4:  # VERIFICADOR
            sql_verif = """
                INSERT INTO verificador (id_usuario, cargo, area)
                VALUES (%s, %s, %s);
            """
            cur.execute(sql_verif, (nuevo_id, "Verificador General", "Bienestar"))

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
