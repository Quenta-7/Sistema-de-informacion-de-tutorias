from flask import Blueprint, request, jsonify
from models.admin_model import (
    obtener_resumen,
    listar_usuarios,
    crear_usuario,
    tutores_disponibles,
    alumnos_disponibles,
    asignar_tutor,
    listar_materias
)

admin_bp = Blueprint("admin", __name__)


# =============================
# RESUMEN DEL DASHBOARD
# =============================
@admin_bp.get("/resumen")
def resumen():
    return jsonify(obtener_resumen())


# =============================
# USUARIOS
# =============================
@admin_bp.get("/usuarios")
def get_usuarios():
    return jsonify({"usuarios": listar_usuarios()})


@admin_bp.post("/usuarios")
def post_usuario():
    data = request.json
    try:
        nuevo = crear_usuario(
            data["nombre"],
            data["apellido"],
            data["email"],
            data["password"],
            data["rol"]
        )
        return jsonify({"message": "Usuario creado", "id": nuevo})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# =============================
# LISTAS PARA ASIGNACIÓN
# =============================
@admin_bp.get("/tutores/disponibles")
def get_tutores_disp():
    return jsonify(tutores_disponibles())


@admin_bp.get("/alumnos/disponibles")
def get_alumnos_disp():
    return jsonify(alumnos_disponibles())

@admin_bp.get("/materias")
def get_materias_disp():
    return jsonify(listar_materias())


@admin_bp.post("/asignar")
def post_asignar():
    data = request.json
    try:
        # Extraemos los 3 datos necesarios
        id_al = data["id_alumno"]
        id_tu = data["id_tutor"]
        id_ma = data.get("id_materia", 1) # Usamos 1 por defecto si no viene
        
        asignar_tutor(id_al, id_tu, id_ma)
        return jsonify({"message": "Asignación realizada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
