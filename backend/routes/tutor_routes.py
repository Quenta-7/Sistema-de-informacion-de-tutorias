from flask import Blueprint, request, jsonify
import models.tutor_model as tutor

tutor_bp = Blueprint("tutor", __name__)

# ======================================================
#   1. ESTUDIANTES ASIGNADOS
# ======================================================
@tutor_bp.route("/estudiantes/<int:id_usuario>", methods=["GET"])
def estudiantes(id_usuario):
    data = tutor.obtener_estudiantes_del_tutor(id_usuario)
    return jsonify({"estudiantes": data})


# ======================================================
#   2. PROXIMAS TUTORIAS
# ======================================================
@tutor_bp.route("/tutorias/<int:id_usuario>", methods=["GET"])
def tutorias(id_usuario):
    data = tutor.obtener_proximas_tutorias(id_usuario)
    return jsonify({"tutorias": data})


# ======================================================
#   3. RETROALIMENTACIONES
# ======================================================
@tutor_bp.route("/retro/<int:id_usuario>", methods=["GET"])
def retroalimentaciones(id_usuario):
    data = tutor.obtener_retroalimentaciones(id_usuario)
    return jsonify({"retroalimentaciones": data})


# ======================================================
#   4. CRONOGRAMAS DISPONIBLES
# ======================================================
@tutor_bp.route("/cronogramas", methods=["GET"])
def cronogramas():
    data = tutor.obtener_cronogramas_tutor()
    return jsonify({"cronogramas": data})


# ======================================================
#   5. MATERIAS ASIGNADAS
# ======================================================
@tutor_bp.route("/materias/<int:id_usuario>", methods=["GET"])
def materias(id_usuario):
    data = tutor.obtener_materias_del_tutor(id_usuario)
    return jsonify({"materias": data})


# ======================================================
#   6. REGISTRAR TUTORIA
# ======================================================
@tutor_bp.route("/registrar", methods=["POST"])
def registrar():
    data = request.get_json()

    ok = tutor.registrar_tutoria(data)
    if ok:
        return jsonify({"message": "Tutoría registrada correctamente"})

    return jsonify({"message": "Error al registrar tutoría"}), 400
