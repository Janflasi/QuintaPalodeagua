// reserva-form.js

document.addEventListener('DOMContentLoaded', function() {
    
    // Animaciones suaves al cargar la página
    function initializeAnimations() {
        const pageHeader = document.querySelector('.page-header');
        const formContainer = document.querySelector('.form-container');
        
        if (pageHeader) {
            pageHeader.style.opacity = '0';
            pageHeader.style.transform = 'translateY(-20px)';
            
            setTimeout(() => {
                pageHeader.style.transition = 'all 0.6s ease-out';
                pageHeader.style.opacity = '1';
                pageHeader.style.transform = 'translateY(0)';
            }, 100);
        }
        
        if (formContainer) {
            formContainer.style.opacity = '0';
            formContainer.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                formContainer.style.transition = 'all 0.6s ease-out';
                formContainer.style.opacity = '1';
                formContainer.style.transform = 'translateY(0)';
            }, 300);
        }
    }
    
    // Mejoras en los campos del formulario
    function enhanceFormFields() {
        const formFields = document.querySelectorAll('.reservation-form input, .reservation-form select, .reservation-form textarea');
        
        formFields.forEach(field => {
            // Animación en focus
            field.addEventListener('focus', function() {
                this.parentElement.classList.add('field-focused');
            });
            
            // Remover animación en blur
            field.addEventListener('blur', function() {
                this.parentElement.classList.remove('field-focused');
                
                // Validar campo si no está vacío
                if (this.value.trim() !== '') {
                    this.classList.add('has-content');
                } else {
                    this.classList.remove('has-content');
                }
            });
            
            // Estado inicial si ya tiene contenido
            if (field.value.trim() !== '') {
                field.classList.add('has-content');
            }
        });
    }
    
    // Mejorar el botón de envío
    function enhanceSubmitButton() {
        const submitBtn = document.querySelector('.btn-submit');
        const form = document.querySelector('.reservation-form');
        
        if (submitBtn && form) {
            form.addEventListener('submit', function(e) {
                // Mostrar estado de carga
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
                submitBtn.disabled = true;
                
                // Simulación de envío (Django manejará el envío real)
                // Esto es solo para la experiencia de usuario
                setTimeout(() => {
                    if (!form.checkValidity()) {
                        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Enviar Solicitud';
                        submitBtn.disabled = false;
                    }
                }, 100);
            });
            
            // Efecto hover mejorado
            submitBtn.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) scale(1.02)';
            });
            
            submitBtn.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        }
    }
    
    // Validación en tiempo real
    function addRealTimeValidation() {
        const formFields = document.querySelectorAll('.reservation-form input[required], .reservation-form select[required], .reservation-form textarea[required]');
        
        formFields.forEach(field => {
            field.addEventListener('input', function() {
                const errorList = this.parentElement.querySelector('.errorlist');
                
                // Remover errores previos si el campo ahora es válido
                if (this.value.trim() !== '' && errorList) {
                    errorList.style.opacity = '0';
                    setTimeout(() => {
                        if (errorList && errorList.parentElement) {
                            errorList.remove();
                        }
                    }, 300);
                }
            });
        });
    }
    
    // Smooth scroll para errores
    function scrollToErrors() {
        const errors = document.querySelectorAll('.errorlist');
        if (errors.length > 0) {
            errors[0].scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }
    }
    
    // Contador de caracteres para textareas
    function addCharacterCounters() {
        const textareas = document.querySelectorAll('.reservation-form textarea');
        
        textareas.forEach(textarea => {
            const maxLength = textarea.getAttribute('maxlength');
            if (maxLength) {
                const counter = document.createElement('div');
                counter.className = 'character-counter';
                counter.style.cssText = `
                    font-size: 0.85rem;
                    color: var(--color-texto-light);
                    text-align: right;
                    margin-top: 0.5rem;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                `;
                
                textarea.parentElement.appendChild(counter);
                
                function updateCounter() {
                    const remaining = maxLength - textarea.value.length;
                    counter.textContent = `${textarea.value.length}/${maxLength} caracteres`;
                    
                    if (remaining < 50) {
                        counter.style.color = '#d32f2f';
                    } else {
                        counter.style.color = 'var(--color-texto-light)';
                    }
                }
                
                textarea.addEventListener('input', updateCounter);
                textarea.addEventListener('focus', () => {
                    counter.style.opacity = '1';
                    updateCounter();
                });
                textarea.addEventListener('blur', () => {
                    counter.style.opacity = '0';
                });
                
                updateCounter();
            }
        });
    }
    
    // Efecto parallax sutil en el header
    function addParallaxEffect() {
        const header = document.querySelector('.page-header');
        if (header) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.2;
                header.style.transform = `translateY(${rate}px)`;
            });
        }
    }
    
    // Inicializar todas las mejoras
    initializeAnimations();
    enhanceFormFields();
    enhanceSubmitButton();
    addRealTimeValidation();
    addCharacterCounters();
    addParallaxEffect();
    
    // Scroll a errores después de cargar la página
    setTimeout(scrollToErrors, 500);
    
    // Agregar clase para animaciones CSS adicionales
    document.body.classList.add('form-enhanced');
});

// CSS adicional para las mejoras de JavaScript
const additionalStyles = `
<style>
.field-focused {
    transform: translateY(-1px);
}

.character-counter {
    transition: all 0.3s ease !important;
}

.form-enhanced .reservation-card {
    animation: slideInUp 0.8s ease-out;
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.btn-submit:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none !important;
}

.errorlist {
    animation: errorSlideIn 0.3s ease-out;
}

@keyframes errorSlideIn {
    from {
        opacity: 0;
        transform: translateX(-10px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}
</style>
`;

// Inyectar estilos adicionales
document.head.insertAdjacentHTML('beforeend', additionalStyles);