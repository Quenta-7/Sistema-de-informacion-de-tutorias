import psycopg2
import bcrypt
from config import Config

def get_connection():
    return psycopg2.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        port=Config.DB_PORT
    )

def verify_user_login(email, password):
    try:
        conn = get_connection()
        cur = conn.cursor()

        sql = """
            SELECT 
                id_usuario,
                id_rol,
                nombre,
                apellido,
                email,
                password_hash
            FROM usuarios
            WHERE email = %s
            LIMIT 1;
        """

        cur.execute(sql, (email,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if not user:
            return None  # usuario no encontrado

        id_usuario, id_rol, nombre, apellido, correo, password_hash = user

        # Convertir si viene como string
        if isinstance(password_hash, str):
            password_hash = password_hash.encode("utf-8")

        # Comparar contraseñas
        if not bcrypt.checkpw(password.encode("utf-8"), password_hash):
            return None

        # Login OK
        return {
            "id_usuario": id_usuario,
            "id_rol": id_rol,
            "nombre": nombre,
            "apellido": apellido,
            "email": correo
        }


    except Exception as e:
        print("Error al verificar usuario:", e)
        return None
