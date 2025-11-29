// ============================
// FRONTEND - Login Script (sin redirección)
// ============================

document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('login-form');
    const tutorIdInput = document.getElementById('tutor_id');
    const passwordInput = document.getElementById('password');
    const messageElement = document.getElementById('message');
    const loginButton = document.getElementById('login-button');

    // Detecta la URL base de Flask según dónde se abra el front-end
    const BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
                     ? 'http://127.0.0.1:5000'
                     : 'http://34.60.247.196:5000';  // Reemplaza con tu IP pública de VM

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        // Limpiar mensajes previos
        messageElement.textContent = '';
        messageElement.className = 'text-center text-sm font-semibold h-4';
        tutorIdInput.classList.remove('input-error');
        passwordInput.classList.remove('input-error');

        const tutor_id = tutorIdInput.value.trim();
        const password = passwordInput.value.trim();

        if (!tutor_id || !password) {
            messageElement.classList.add('text-red-600');
            messageElement.textContent = 'Por favor, complete todos los campos.';
            tutorIdInput.classList.add('input-error');
            passwordInput.classList.add('input-error');
            return;
        }

        loginButton.disabled = true;
        loginButton.textContent = 'Verificando...';

        try {
            const response = await fetch(`${BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tutor_id, password })
            });

            const result = await response.json();

            if (response.ok) {
                messageElement.classList.add('text-green-600');
                messageElement.textContent = `¡Bienvenido! Rol: ${result.user.rol}`;
                loginButton.textContent = 'Éxito ✅';

                // Guardar datos del usuario localmente (opcional)
                localStorage.setItem('userData', JSON.stringify(result.user));
            } else {
                messageElement.classList.add('text-red-600');
                messageElement.textContent = result.message || 'Usuario o contraseña incorrectos.';
                tutorIdInput.classList.add('input-error');
                passwordInput.classList.add('input-error');
                loginButton.textContent = 'Iniciar Sesión';
            }

        } catch (error) {
            console.error('Error de conexión con el servidor:', error);
            messageElement.classList.add('text-red-600');
            messageElement.textContent = 'No se pudo conectar al servidor Flask (Puerto 5000).';
            loginButton.textContent = 'Iniciar Sesión';
        } finally {
            loginButton.disabled = false;
        }
    });
});
