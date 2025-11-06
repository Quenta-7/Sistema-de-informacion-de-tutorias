# backend/models/user_model.py

import psycopg2
from config import Config
# FUNCIÓN 1: get_db_connection() DEBE ESTAR DEFINIDA AQUÍ
def get_db_connection():
    """Establece y retorna una conexión a la base de datos PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
def verify_user_login(tutor_id, password):
    """Verifica si las credenciales de un usuario son válidas."""
    conn = get_db_connection()
    user = None
    
    if conn:
        try:
            cursor = conn.cursor()
            # Esta línea es un comentario explicativo y puede quedarse con el '#'
            # Asumiendo que el campo para el login es 'tutor_id' y 'descripcion'
            
            # Estas dos líneas deben estar indentadas dentro del bloque try:
            query = "SELECT id, rol FROM usuarios WHERE id = %s AND contrasena = %s" 
            cursor.execute(query, (tutor_id, password))
            
            result = cursor.fetchone()
            if result:
                user = {"id": result[0], "rol": result[1]}
            
            cursor.close()
        except Exception as e:
            print(f"Error al verificar usuario: {e}")
        finally:
            conn.close()
            
    return user