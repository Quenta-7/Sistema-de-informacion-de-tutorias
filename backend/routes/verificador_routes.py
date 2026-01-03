from flask import Blueprint, jsonify
import models.verificador_model as veri

verificador_bp = Blueprint("verificador", __name__)

@verificador_bp.route("/fecha/<string:fecha>", methods=["GET"])
def por_fecha(fecha):
    data = veri.tutorias_por_fecha(fecha)
    return jsonify({"tutorias": data})

@verificador_bp.route("/semestre/<string:sem>", methods=["GET"])
def por_semestre(sem):
    data = veri.tutorias_por_semestre(sem)
    return jsonify({"tutorias": data})

@verificador_bp.route("/alumno/<int:id_usuario>", methods=["GET"])
def seguimiento(id_usuario):
    # Llama a la nueva función que agregamos al modelo
    data = veri.seguimiento_por_alumno(id_usuario)
    return jsonify({"seguimiento": data})