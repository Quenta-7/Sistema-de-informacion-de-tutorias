# backend/app.py

from flask import Flask, send_from_directory
from flask_cors import CORS
from controllers.auth_controller import auth_bp

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

# Registrar Blueprint
app.register_blueprint(auth_bp, url_prefix="/api/auth")

# --------------------------
#  RUTAS PRINCIPALES
# --------------------------

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

# Para servir JS, CSS, imágenes
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
