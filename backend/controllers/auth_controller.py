from flask import Blueprint, request, jsonify, session
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
        # GUARDAR EN SESIÓN DEL SERVIDOR
        session['user_id'] = user["id_usuario"]
        session['rol'] = user["id_rol"]
        session['nombre'] = user["nombre"]

        return jsonify({
            "message": "Login exitoso",
            "user": {
                "id": user["id_usuario"],
                "email": user["email"],
                "rol": user["id_rol"],
                "nombre": user["nombre"],
                "apellido": user["apellido"]
            }
        }), 200

    return jsonify({"message": "Usuario o contraseña incorrectos"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear() # Limpia la sesión del servidor
    return jsonify({"message": "Sesión cerrada"}), 200
