from flask import Blueprint, request, jsonify
from models.user_model import verify_user_login

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Faltan credenciales"}), 400

    user = verify_user_login(email, password)

    if user:
        return jsonify({
            "message": "Login exitoso",
            "user": {
                "id": user["id_usuario"],
                "email": user["email"],
                "rol": user["id_rol"],   # ← YA ES rol REAL
                "nombre": user["nombre"],
                "apellido": user["apellido"]
            }
        }), 200

    return jsonify({"message": "Usuario o contraseña incorrectos"}), 401
