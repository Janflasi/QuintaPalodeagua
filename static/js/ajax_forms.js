// static/js/ajax_forms.js

document.addEventListener('DOMContentLoaded', function() {
    const reservaForm = document.getElementById('reserva-form');
    const formMessages = document.getElementById('form-messages');
    
    if (!reservaForm) return;

    reservaForm.addEventListener('submit', function(e) {
        // 1. Prevenir el envío normal del formulario (que recarga la página)
        e.preventDefault();

        // Mostrar un estado de "cargando"
        const submitButton = reservaForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.textContent = 'Enviando...';
        formMessages.innerHTML = '';

        // 2. Recopilar los datos del formulario
        const formData = new FormData(reservaForm);

        // 3. Enviar los datos usando la Fetch API de JavaScript
        fetch(reservaForm.action, {
            method: 'POST',
            headers: {
                // El header 'X-Requested-With' le dice a Django que esta es una petición AJAX
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // 4. Manejar la respuesta del servidor
            if (data.success) {
                // Si todo salió bien
                formMessages.innerHTML = `
                    <div class="alert alert-success">${data.message}</div>
                `;
                reservaForm.reset(); // Limpiar el formulario
                // Opcional: Redirigir al panel después de 2 segundos
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 2000);
            } else {
                // Si hubo errores de validación
                let errorHtml = '<div class="alert alert-danger"><ul>';
                for (const field in data.errors) {
                    errorHtml += `<li>${data.errors[field][0]}</li>`;
                }
                errorHtml += '</ul></div>';
                formMessages.innerHTML = errorHtml;
                
                // Reactivar el botón
                submitButton.disabled = false;
                submitButton.textContent = 'Enviar Solicitud';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            formMessages.innerHTML = '<div class="alert alert-danger">Ocurrió un error inesperado. Por favor, inténtalo de nuevo.</div>';
            submitButton.disabled = false;
            submitButton.textContent = 'Enviar Solicitud';
        });
    });
});