# backend/controllers/auth_controller.py

from flask import Blueprint, request, jsonify
from models.user_model import verify_user_login # Importa la función de tu modelo

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    # Obtiene los datos JSON enviados desde el formulario HTML/JS
    data = request.get_json()
    id = data.get('id')
    password = data.get('contraseña')

    if not id or not password:
        return jsonify({"message": "Faltan credenciales"}), 400

    # Llama al modelo para verificar las credenciales
    user = verify_user_login(id, password)

    if user:
        # Login exitoso (código de estado 200)
        # En una aplicación real se usaría JWT
        return jsonify({"message": "Login exitoso", "user": user}), 200
    else:
        # Login fallido (código de estado 401: Unauthorized)
        return jsonify({"message": "Usuario o contraseña incorrectos"}), 401