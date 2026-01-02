from flask import Flask, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from controllers.auth_controller import auth_bp
from routes.tutor_routes import tutor_bp
from routes.admin_routes import admin_bp
from routes.estudiante_routes import estudiante_bp
from routes.verificador_routes import verificador_bp

app = Flask(__name__, static_folder="../frontend", static_url_path="")
app.secret_key = 'tu_llave_secreta_aqui'  # NECESARIO PARA SESIONES
CORS(app)

# Registro de Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(tutor_bp, url_prefix="/api/tutor")
if admin_bp: app.register_blueprint(admin_bp, url_prefix="/api/admin")
if estudiante_bp: app.register_blueprint(estudiante_bp, url_prefix="/api/estudiante")
if verificador_bp: app.register_blueprint(verificador_bp, url_prefix="/api/verificador")

# --- RUTAS PROTEGIDAS DEL FRONTEND ---

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/admin")
def admin_dashboard():
    # Verifica si hay sesión y si el rol es 1 (Admin)
    if 'user_id' not in session or session.get('rol') != 1:
        return redirect(url_for('home'))
    return send_from_directory(app.static_folder, "dashboard.html")

@app.route("/tutor")
def tutor_dashboard():
    # Verifica si hay sesión y si el rol es 2 (Tutor)
    if 'user_id' not in session or session.get('rol') != 2:
        return redirect(url_for('home'))
    return send_from_directory(app.static_folder, "dashboard_tutor.html")



@app.route("/estudiante")
def estudiante_dashboard():
    # Verifica si hay sesión y si el rol es 3 (Estudiante)
    if 'user_id' not in session or session.get('rol') != 3:
        return redirect(url_for('home'))
    return send_from_directory(app.static_folder, "dashboard_estudiante.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)