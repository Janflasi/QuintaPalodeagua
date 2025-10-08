// gestionar_usuarios.js

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar iconos de Feather (si está disponible)
    if (typeof feather !== 'undefined') {
        feather.replace();
    }

    // Confirmación antes de cambiar el estado de un usuario
    const formsToggle = document.querySelectorAll('.form-toggle');
    
    formsToggle.forEach(form => {
        form.addEventListener('submit', function(e) {
            const button = this.querySelector('.btn-action');
            const action = button.textContent.trim();
            const row = this.closest('tr');
            const username = row.querySelector('.username').textContent;
            
            const mensaje = action === 'Desactivar' 
                ? `¿Estás seguro de que deseas desactivar al usuario "${username}"?`
                : `¿Estás seguro de que deseas activar al usuario "${username}"?`;
            
            if (!confirm(mensaje)) {
                e.preventDefault();
            }
        });
    });

    // Animación suave al cargar la tabla
    const rows = document.querySelectorAll('.usuario-row');
    rows.forEach((row, index) => {
        row.style.opacity = '0';
        row.style.transform = 'translateY(10px)';
        
        setTimeout(() => {
            row.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
        }, index * 50);
    });

    // Efecto de ripple en los botones (opcional)
    function createRipple(event) {
        const button = event.currentTarget;
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        
        const existingRipple = button.querySelector('.ripple');
        if (existingRipple) {
            existingRipple.remove();
        }
        
        button.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
    
    // Agregar estilo para el efecto ripple
    const style = document.createElement('style');
    style.textContent = `
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Aplicar ripple a los botones
    const buttons = document.querySelectorAll('.btn-action, .btn-crear');
    buttons.forEach(button => {
        button.addEventListener('click', createRipple);
    });

    // Búsqueda en tiempo real (opcional - requiere agregar input de búsqueda)
    const searchInput = document.querySelector('.search-usuarios');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            
            rows.forEach(row => {
                const username = row.querySelector('.username').textContent.toLowerCase();
                const email = row.querySelector('.email').textContent.toLowerCase();
                
                if (username.includes(searchTerm) || email.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Scroll suave al inicio
    const scrollToTop = document.querySelector('.scroll-to-top');
    if (scrollToTop) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollToTop.style.display = 'flex';
            } else {
                scrollToTop.style.display = 'none';
            }
        });
        
        scrollToTop.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});