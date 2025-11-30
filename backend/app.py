from flask import Flask, send_from_directory
from flask_cors import CORS

# ======================================
#   IMPORTAR BLUEPRINTS
# ======================================

# Autenticación
from controllers.auth_controller import auth_bp

# Tutor
from routes.tutor_routes import tutor_bp


# Intentar cargar admin, estudiante y verificador
try:
    from routes.admin_routes import admin_bp
except Exception as e:
    print("⚠ ERROR cargando admin_routes:", e)
    admin_bp = None

try:
    from routes.estudiante_routes import estudiante_bp
    print(">>> estudiante_routes IMPORTADO correctamente")
except Exception as e:
    print("⚠ ERROR cargando estudiante_routes:", e)
    estudiante_bp = None

try:
    from routes.verificador_routes import verificador_bp
except Exception as e:
    print("⚠ ERROR cargando verificador_routes:", e)
    verificador_bp = None


# ======================================
#   CREAR APP
# ======================================
app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)


# ======================================
#   REGISTRO DE BLUEPRINTS
# ======================================
app.register_blueprint(auth_bp, url_prefix="/api/auth")
print("✔ Blueprint AUTH registrado")

app.register_blueprint(tutor_bp, url_prefix="/api/tutor")
print("✔ Blueprint TUTOR registrado")

if admin_bp:
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    print("✔ Blueprint ADMIN registrado")
else:
    print("❌ Blueprint ADMIN NO registrado")

if estudiante_bp:
    app.register_blueprint(estudiante_bp, url_prefix="/api/estudiante")
    print("✔ Blueprint ESTUDIANTE registrado")
else:
    print("❌ Blueprint ESTUDIANTE NO registrado")

if verificador_bp:
    app.register_blueprint(verificador_bp, url_prefix="/api/verificador")
    print("✔ Blueprint VERIFICADOR registrado")
else:
    print("❌ Blueprint VERIFICADOR NO registrado")


# ======================================
#   RUTAS DEL FRONTEND
# ======================================

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/admin")
def admin_dashboard():
    return send_from_directory(app.static_folder, "dashboard.html")

@app.route("/tutor")
def tutor_dashboard():
    return send_from_directory(app.static_folder, "dashboard_tutor.html")

@app.route("/estudiante")
def estudiante_dashboard():
    return send_from_directory(app.static_folder, "dashboard_estudiante.html")

@app.route("/verificador")
def verificador_dashboard():
    return send_from_directory(app.static_folder, "dashboard_verificador.html")


# Archivos estáticos (CSS, JS, imágenes, etc.)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)


# ======================================
#   EJECUCIÓN DEL SERVIDOR
# ======================================
if __name__ == "__main__":
    print("\n=======================================")
    print("   SERVIDOR INICIADO CORRECTAMENTE")
    print("   URL: http://localhost:8080")
    print("=======================================\n")
    app.run(host="0.0.0.0", port=8080)
