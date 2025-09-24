// static/js/login.js

document.addEventListener('DOMContentLoaded', function() {
    
    // Inicializar iconos de Feather
    feather.replace();
    
    // --- TOGGLE DE CONTRASEÑA ---
    const passwordToggle = document.getElementById('togglePassword');
    const passwordField = document.querySelector('input[type="password"]');
    
    if (passwordToggle && passwordField) {
        passwordToggle.addEventListener('click', function() {
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            
            // Cambiar icono
            const icon = this.querySelector('.toggle-icon');
            if (type === 'text') {
                icon.setAttribute('data-feather', 'eye-off');
            } else {
                icon.setAttribute('data-feather', 'eye');
            }
            feather.replace();
            
            // Efecto visual
            this.style.transform = 'scale(0.9)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    }
    
    // --- VALIDACIÓN EN TIEMPO REAL ---
    const formInputs = document.querySelectorAll('.login-form input');
    
    formInputs.forEach(input => {
        // Efectos de focus
        input.addEventListener('focus', function() {
            this.parentNode.classList.add('focused');
            
            // Animación del ícono
            const icon = this.parentNode.querySelector('.label-icon');
            if (icon) {
                icon.style.transform = 'translateY(-50%) scale(1.1)';
                icon.style.color = 'var(--color-principal)';
            }
        });
        
        input.addEventListener('blur', function() {
            this.parentNode.classList.remove('focused');
            
            // Restaurar ícono
            const icon = this.parentNode.querySelector('.label-icon');
            if (icon) {
                icon.style.transform = 'translateY(-50%) scale(1)';
                if (!this.value) {
                    icon.style.color = 'var(--color-texto-light)';
                }
            }
            
            // Validación básica
            validateField(this);
        });
        
        // Validación en tiempo real mientras escribe
        input.addEventListener('input', function() {
            clearTimeout(this.validationTimeout);
            this.validationTimeout = setTimeout(() => {
                validateField(this);
            }, 500);
        });
    });
    
    // Función de validación
    function validateField(field) {
        const value = field.value.trim();
        const fieldType = field.type;
        let isValid = true;
        let errorMessage = '';
        
        // Limpiar errores previos
        const existingError = field.parentNode.querySelector('.form-error');
        if (existingError) {
            existingError.remove();
        }
        
        field.classList.remove('is-valid', 'is-invalid');
        
        if (value === '') {
            return; // No validar campos vacíos hasta el envío
        }
        
        // Validación por tipo de campo
        if (fieldType === 'text' || field.name === 'username') {
            if (value.length < 3) {
                isValid = false;
                errorMessage = 'El usuario debe tener al menos 3 caracteres';
            }
        } else if (fieldType === 'password') {
            if (value.length < 6) {
                isValid = false;
                errorMessage = 'La contraseña debe tener al menos 6 caracteres';
            }
        }
        
        // Aplicar estilos de validación
        if (isValid) {
            field.classList.add('is-valid');
            
            // Icono de éxito
            const icon = field.parentNode.querySelector('.label-icon');
            if (icon) {
                icon.style.color = 'var(--color-success)';
            }
        } else {
            field.classList.add('is-invalid');
            
            // Mostrar error
            const errorDiv = document.createElement('div');
            errorDiv.className = 'form-error';
            errorDiv.innerHTML = `
                <span data-feather="alert-circle" class="error-icon"></span>
                ${errorMessage}
            `;
            field.parentNode.appendChild(errorDiv);
            feather.replace();
        }
    }
    
    // --- ANIMACIÓN DEL FORMULARIO AL ENVIAR ---
    const loginForm = document.querySelector('.login-form');
    const submitButton = document.querySelector('.btn-login');
    
    if (loginForm && submitButton) {
        loginForm.addEventListener('submit', function(e) {
            // Animación de carga
            submitButton.classList.add('loading');
            submitButton.disabled = true;
            
            // Validar todos los campos antes del envío
            let allValid = true;
            const inputs = this.querySelectorAll('input[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    allValid = false;
                    input.classList.add('is-invalid');
                    
                    // Crear error si no existe
                    const existingError = input.parentNode.querySelector('.form-error');
                    if (!existingError) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'form-error';
                        errorDiv.innerHTML = `
                            <span data-feather="alert-circle" class="error-icon"></span>
                            Este campo es obligatorio
                        `;
                        input.parentNode.appendChild(errorDiv);
                        feather.replace();
                    }
                }
            });
            
            if (!allValid) {
                e.preventDefault();
                submitButton.classList.remove('loading');
                submitButton.disabled = false;
                
                // Scroll al primer error
                const firstError = this.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
            
            // Si hay errores del servidor, quitar loading
            setTimeout(() => {
                if (document.querySelector('.form-error-general')) {
                    submitButton.classList.remove('loading');
                    submitButton.disabled = false;
                }
            }, 100);
        });
    }
    
    // --- ANIMACIONES DE ENTRADA ---
    const loginCard = document.querySelector('.login-card');
    if (loginCard) {
        // Observador para animar cuando sea visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationDelay = '0.2s';
                    entry.target.classList.add('animate-in');
                }
            });
        }, { threshold: 0.1 });
        
        observer.observe(loginCard);
    }
    
    // --- EFECTOS DE PARTÍCULAS SUAVES (OPCIONAL) ---
    function createFloatingParticles() {
        const container = document.querySelector('.login-bg-decoration');
        if (!container) return;
        
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                const particle = document.createElement('div');
                particle.className = 'floating-particle';
                particle.style.cssText = `
                    position: absolute;
                    width: 4px;
                    height: 4px;
                    background: var(--color-principal-light);
                    border-radius: 50%;
                    opacity: 0.3;
                    left: ${Math.random() * 100}%;
                    top: ${Math.random() * 100}%;
                    animation: floatUp ${3 + Math.random() * 2}s linear infinite;
                `;
                
                container.appendChild(particle);
                
                // Remover después de la animación
                setTimeout(() => {
                    if (particle.parentNode) {
                        particle.remove();
                    }
                }, 5000);
            }, i * 1000);
        }
    }
    
    // Crear partículas cada 10 segundos
    createFloatingParticles();
    setInterval(createFloatingParticles, 10000);
    
    // --- MANEJO DE ERRORES EXISTENTES ---
    const existingErrors = document.querySelectorAll('.form-error, .form-error-general');
    existingErrors.forEach(error => {
        // Animación de entrada para errores
        error.style.opacity = '0';
        error.style.transform = 'translateY(-10px)';
        
        setTimeout(() => {
            error.style.transition = 'all 0.3s ease';
            error.style.opacity = '1';
            error.style.transform = 'translateY(0)';
        }, 100);
    });
    
    // --- AUTOCOMPLETAR MEJORADO ---
    const usernameField = document.querySelector('input[name="username"]');
    if (usernameField) {
        usernameField.addEventListener('input', function() {
            // Guardar en localStorage para sugerencias futuras (opcional)
            if (this.value.length >= 3) {
                localStorage.setItem('lastUsername', this.value);
            }
        });
        
        // Cargar último usuario (opcional)
        const lastUsername = localStorage.getItem('lastUsername');
        if (lastUsername && !usernameField.value) {
            usernameField.setAttribute('placeholder', `Ej: ${lastUsername}`);
        }
    }
    
    // --- TECLAS RÁPIDAS ---
    document.addEventListener('keydown', function(e) {
        // Enter en username va a password
        if (e.key === 'Enter' && e.target.name === 'username') {
            e.preventDefault();
            const passwordField = document.querySelector('input[name="password"]');
            if (passwordField) {
                passwordField.focus();
            }
        }
        
        // Ctrl/Cmd + Enter envía el formulario
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const form = document.querySelector('.login-form');
            if (form) {
                form.submit();
            }
        }
    });
    
    console.log('🔐 Sistema de login inicializado correctamente');
});

// Animación CSS para partículas flotantes
const style = document.createElement('style');
style.textContent = `
    @keyframes floatUp {
        0% {
            opacity: 0.3;
            transform: translateY(0) rotate(0deg);
        }
        50% {
            opacity: 0.6;
        }
        100% {
            opacity: 0;
            transform: translateY(-100px) rotate(360deg);
        }
    }
    
    .animate-in {
        animation: cardAppear 0.8s ease-out forwards;
    }
`;
document.head.appendChild(style);