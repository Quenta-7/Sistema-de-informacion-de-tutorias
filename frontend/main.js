// frontend/assets/js/main.js

document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Evita que la página se recargue

    const id = document.getElementById('id').value;
    const password = document.getElementById('contraseña').value;
    const messageElement = document.getElementById('message');
    
    messageElement.textContent = ''; // Limpiar mensajes

    try {
        // Petición POST al endpoint de Flask
        const response = await fetch('http://localhost:5000/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id, password })
        });

        const result = await response.json();

        if (response.ok) {
            messageElement.style.color = 'green';
            messageElement.textContent = result.message + `. Rol: ${result.user.rol}`;
            // Aquí debes redirigir al usuario
            // Ejemplo: window.location.href = 'dashboard.html'; 
            console.log("Login exitoso:", result.user);
        } else {
            messageElement.style.color = 'red';
            messageElement.textContent = result.message || 'Error desconocido.';
        }
    } catch (error) {
        console.error('Error de conexión con el servidor:', error);
        messageElement.style.color = 'red';
        messageElement.textContent = 'No se pudo conectar al servidor (Verifique que Flask esté corriendo).';
    }
});