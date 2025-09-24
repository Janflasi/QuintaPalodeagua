// static/js/register.js

document.addEventListener('DOMContentLoaded', function() {
    // Activar íconos de Feather
    feather.replace();

    // Lógica para etiquetas flotantes
    const inputs = document.querySelectorAll('.form-group-modern .form-control');
    inputs.forEach(input => {
        // Para que la etiqueta se mantenga arriba si el campo ya tiene valor (ej. al recargar con error)
        if (input.value) {
            input.classList.add('has-value');
        }
        input.addEventListener('input', () => {
            if (input.value) {
                input.classList.add('has-value');
            } else {
                input.classList.remove('has-value');
            }
        });
    });
    
    // Lógica para mostrar/ocultar contraseña
    const visibilityToggles = document.querySelectorAll('.password-visibility');
    visibilityToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const targetId = this.dataset.target;
            const passwordInput = document.getElementById(targetId);
            const icon = this.querySelector('.visibility-icon');

            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.setAttribute('data-feather', 'eye-off');
            } else {
                passwordInput.type = 'password';
                icon.setAttribute('data-feather', 'eye');
            }
            feather.replace(); // Volver a renderizar el ícono cambiado
        });
    });

    // Lógica para fortaleza de contraseña
    const passwordField = document.getElementById('id_password1');
    const strengthFill = document.querySelector('.strength-fill');
    const strengthText = document.querySelector('.strength-text');

    if (passwordField) {
        passwordField.addEventListener('input', function() {
            const pass = this.value;
            let score = 0;
            if (pass.length > 8) score++;
            if (pass.match(/[a-z]/)) score++;
            if (pass.match(/[A-Z]/)) score++;
            if (pass.match(/[0-9]/)) score++;
            if (pass.match(/[^a-zA-Z0-9]/)) score++;

            switch (score) {
                case 0:
                case 1:
                    strengthFill.style.width = '20%';
                    strengthFill.style.backgroundColor = 'red';
                    strengthText.textContent = 'Muy débil';
                    break;
                case 2:
                    strengthFill.style.width = '40%';
                    strengthFill.style.backgroundColor = 'orange';
                    strengthText.textContent = 'Débil';
                    break;
                case 3:
                    strengthFill.style.width = '60%';
                    strengthFill.style.backgroundColor = 'yellow';
                    strengthText.textContent = 'Aceptable';
                    break;
                case 4:
                    strengthFill.style.width = '80%';
                    strengthFill.style.backgroundColor = 'lightgreen';
                    strengthText.textContent = 'Fuerte';
                    break;
                case 5:
                    strengthFill.style.width = '100%';
                    strengthFill.style.backgroundColor = 'green';
                    strengthText.textContent = 'Muy fuerte';
                    break;
            }
        });
    }

    // Lógica para verificar que las contraseñas coinciden
    const passwordConfirmField = document.getElementById('id_password2');
    const matchDiv = document.getElementById('password-match');
    
    if (passwordField && passwordConfirmField) {
        function checkMatch() {
            if (passwordConfirmField.value === '') {
                matchDiv.textContent = '';
                return;
            }
            if (passwordField.value === passwordConfirmField.value) {
                matchDiv.textContent = '✅';
            } else {
                matchDiv.textContent = '❌';
            }
        }
        passwordField.addEventListener('input', checkMatch);
        passwordConfirmField.addEventListener('input', checkMatch);
    }
});