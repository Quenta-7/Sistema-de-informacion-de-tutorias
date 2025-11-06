# backend/app.py

from flask import Flask
from controllers.auth_controller import auth_bp
from flask_cors import CORS # Importa CORS para permitir comunicación con el front-end

app = Flask(__name__)
# Habilita CORS para permitir peticiones desde el navegador (frontend)
CORS(app) 

# Registrar el Blueprint de autenticación. Todas las rutas empezarán con /api/auth
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/')
def home():
    return "Servidor del Sistema de Tutorías en funcionamiento"

if __name__ == '__main__':
    # Ejecuta el servidor en el puerto 5000 (diferente al puerto de Postgres)
    app.run(debug=True, port=5000)