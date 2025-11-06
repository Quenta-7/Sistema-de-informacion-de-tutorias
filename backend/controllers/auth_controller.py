# backend/controllers/auth_controller.py

from flask import Blueprint, request, jsonify
from models.user_model import verify_user_login  # Importa la función de tu modelo

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    # Obtiene los datos JSON enviados desde el formulario HTML/JS
    data = request.get_json()
    tutor_id = data.get('tutor_id')
    password = data.get('password')

    if not tutor_id or not password:
        return jsonify({"message": "Faltan credenciales"}), 400

    # Llama al modelo para verificar las credenciales
    user = verify_user_login(tutor_id, password)

    if user:
        return jsonify({
            "message": "Login exitoso",
            "user": user
        }), 200
    else:
        return jsonify({"message": "Usuario o contraseña incorrectos"}), 401
