# backend/controllers/auth_controller.py

from flask import Blueprint, request, jsonify
from models.user_model import verify_user_login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    tutor_id = data.get('tutor_id')
    password = data.get('password')

    if not tutor_id or not password:
        return jsonify({"message": "Faltan credenciales"}), 400

    user = verify_user_login(tutor_id, password)

    if user:
        return jsonify({
            "message": "Login exitoso",
            "rol": user["rol"],  # IMPORTANTE para redirigir en frontend
            "user": user
        }), 200
    
    return jsonify({"message": "Usuario o contraseña incorrectos"}), 401
