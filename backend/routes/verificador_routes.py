from flask import Blueprint, jsonify
import models.verificador_model as veri

verificador_bp = Blueprint("verificador", __name__)

# ======================================================
#   1. TUTORIAS POR FECHA
# ======================================================
@verificador_bp.route("/fecha/<string:fecha>", methods=["GET"])
def por_fecha(fecha):
    data = veri.tutorias_por_fecha(fecha)
    return jsonify({"tutorias": data})


# ======================================================
#   2. TUTORIAS POR SEMESTRE
# ======================================================
@verificador_bp.route("/semestre/<string:sem>", methods=["GET"])
def por_semestre(sem):
    data = veri.tutorias_por_semestre(sem)
    return jsonify({"tutorias": data})


# ======================================================
#   3. SEGUIMIENTO POR ALUMNO
# ======================================================
@verificador_bp.route("/alumno/<int:id_usuario>", methods=["GET"])
def seguimiento(id_usuario):
    data = veri.seguimiento_por_alumno(id_usuario)
    return jsonify({"seguimiento": data})
