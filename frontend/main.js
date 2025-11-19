// ============================
// FRONTEND - Login Script
// ============================
// Este script maneja el envío del formulario de login
// y la comunicación con el backend Flask.

document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('login-form');
    const tutorIdInput = document.getElementById('tutor_id');
    const passwordInput = document.getElementById('password');
    const messageElement = document.getElementById('message');
    const loginButton = document.getElementById('login-button');

    // Evento de envío del formulario
    form.addEventListener('submit', async function (event) {
        event.preventDefault(); // Evita recargar la página

        // Limpiar mensajes y estilos previos
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

        // Deshabilita botón mientras se verifica
        loginButton.disabled = true;
        loginButton.textContent = 'Verificando...';

        try {
            // Petición POST al backend Flask
            const response = await fetch('http://localhost:5000/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tutor_id, password })
            });

            const result = await response.json();

            if (response.ok) {
                // ✅ Login exitoso
                messageElement.classList.add('text-green-600');
                messageElement.textContent = `¡Bienvenido! Rol: ${result.user.rol}`;
                loginButton.textContent = 'Éxito ✅';

                // ✅ Guarda los datos del usuario localmente
                localStorage.setItem('userData', JSON.stringify(result.user));

                // 🕒 Redirección al dashboard según rol
                setTimeout(() => {
                    console.log("Intentando redirigir...");

                    let destino;

                    if (result.user.rol === 'administrador') {
                        destino = `${window.location.origin}/admin`;
                    } else if (result.user.rol === 'tutor') {
                        destino = `${window.location.origin}/tutor`;
                    } 
                    else if (result.user.rol === 'estudiante') {
                        destino = `${window.location.origin}/estudiante`;
                    } 
                    else if (result.user.rol === 'verificador'){
                        destino = `${window.location.origin}/verificador`;
                    }
                    else {
                        destino = `${window.location.origin}/`;
                    }
                    
                    console.log("Redirigiendo a:", destino);
                    window.location.href = destino;
                }, 1500); // 1.5 segundos para mostrar el mensaje de éxito

            } else {
                // ❌ Error en autenticación
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
