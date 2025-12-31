from flask import Blueprint, jsonify
from models.estudiante_model import (
    obtener_tutor_asignado,
    obtener_horario_estudiante,
    obtener_retroalimentaciones
)

# NOMBRE CORRECTO DEL BLUEPRINT
estudiante_bp = Blueprint("estudiante", __name__)
print(">>> Blueprint ESTUDIANTE CARGADO correctamente")

# ================================
#    TUTOR ASIGNADO
# ================================
@estudiante_bp.route("/tutor/<int:id_usuario>", methods=["GET"])
def tutor_asignado(id_usuario):
    print(">>> Ruta /tutor ejecutada con id:", id_usuario)
    tutor = obtener_tutor_asignado(id_usuario)
    return jsonify({"tutor": tutor}), 200


# ================================
#    HORARIO DEL ESTUDIANTE
# ================================
@estudiante_bp.route("/horario/<int:id_usuario>", methods=["GET"])
def horario_estudiante(id_usuario):
    print(">>> Ruta /horario ejecutada con id:", id_usuario)
    horario = obtener_horario_estudiante(id_usuario)
    return jsonify({"horario": horario}), 200


# ================================
#    RETROALIMENTACIONES
# ================================
@estudiante_bp.route("/retro/<int:id_usuario>", methods=["GET"])
def retroalimentaciones(id_usuario):
    print(">>> Ruta /retro ejecutada con id:", id_usuario)
    retro = obtener_retroalimentaciones(id_usuario)
    return jsonify({"retroalimentaciones": retro}), 200
