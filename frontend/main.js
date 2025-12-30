document.addEventListener("DOMContentLoaded", () => {

    console.log("Login JS cargado correctamente.");

    const form = document.getElementById("login-form");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const messageElement = document.getElementById("message");
    const loginButton = document.getElementById("login-button");

    if (!form) {
        console.error("ERROR: No existe el formulario con id='login-form'");
        return;
    }

   
    // Detectar si es local o producción de forma automática
    const BASE_URL = window.location.origin;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        if (!email || !password) {
            messageElement.textContent = "Complete todos los campos.";
            return;
        }

        loginButton.disabled = true;
        loginButton.textContent = "Verificando...";

        try {
            const response = await fetch(`${BASE_URL}/api/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            const result = await response.json();
            console.log("Respuesta backend:", result);

            if (!response.ok) {
                messageElement.textContent = result.message || "Usuario o contraseña incorrectos.";
                loginButton.disabled = false;
                loginButton.textContent = "Iniciar Sesión";
                return;
            }

            // ================================
            //  NORMALIZAR OBJETO USUARIO
            // ================================
            const rol = Number(result.user.rol || result.user.id_rol);

            const userData = {
                id: result.user.id || result.user.id_usuario,
                nombre: result.user.nombre,
                apellido: result.user.apellido,
                email: result.user.email,
                rol: rol,
            };

            console.log("Usuario normalizado:", userData);

            // Guardar usuario normalizado
            localStorage.setItem("userData", JSON.stringify(userData));

            // ================================
            //  REDIRECCIÓN SEGÚN ROL
            // ================================
            switch (rol) {
                case 1:
                    window.location.href = "/admin";
                    break;
                case 2:
                    window.location.href = "/tutor";
                    break;
                case 3:
                    window.location.href = "/estudiante";
                    break;
                case 4:
                    window.location.href = "/verificador";
                    break;
                default:
                    console.warn("ROL NO RECONOCIDO:", rol);
                    window.location.href = "/";
            }

        } catch (error) {
            console.error("Error de conexión:", error);
            messageElement.textContent = "No se pudo conectar al servidor.";
        }

        loginButton.disabled = false;
        loginButton.textContent = "Iniciar Sesión";
    });
});
