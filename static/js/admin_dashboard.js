// static/js/admin_dashboard.js

document.addEventListener('DOMContentLoaded', function() {
    
    // Inicializar iconos de Feather
    feather.replace();
    
    // --- ANIMACIÓN DE CONTADORES ---
    function animateValue(element, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const value = Math.floor(progress * (end - start) + start);
            element.textContent = value;
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
    
    // Animar los valores de las cards
    const statValues = document.querySelectorAll('.stat-card-value');
    statValues.forEach(stat => {
        const targetValue = parseInt(stat.textContent);
        if (!isNaN(targetValue)) {
            stat.textContent = '0';
            setTimeout(() => {
                animateValue(stat, 0, targetValue, 1500);
            }, 300);
        }
    });
    
    // --- EFECTOS HOVER EN LAS CARDS ---
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            const icon = this.querySelector('.stat-card-icon');
            if (icon) {
                icon.style.transform = 'scale(1.1) rotate(5deg)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            const icon = this.querySelector('.stat-card-icon');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });
    });
    
    // --- ANIMACIÓN DE ENTRADA CON INTERSECTION OBSERVER ---
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observar cards para animación de entrada
    statCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        observer.observe(card);
    });
    
    // --- EFECTO RIPPLE EN CARDS AL HACER CLICK ---
    statCards.forEach(card => {
        card.addEventListener('click', function(e) {
            const ripple = document.createElement('div');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.4);
                left: ${x}px;
                top: ${y}px;
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // --- ACTUALIZACIÓN PERIÓDICA (OPCIONAL) ---
    function refreshDashboard() {
        // Aquí puedes agregar lógica para actualizar los datos vía AJAX
        console.log('Dashboard actualizado');
        
        // Efecto visual de actualización
        statCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.animation = 'none';
                setTimeout(() => {
                    card.style.animation = 'fadeInUp 0.6s ease-out';
                }, 10);
            }, index * 100);
        });
    }
    
    // Actualizar cada 5 minutos (opcional)
    // setInterval(refreshDashboard, 300000);
    
    // --- FORMATO DE NÚMEROS CON SEPARADORES ---
    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
    
    statValues.forEach(stat => {
        const value = parseInt(stat.textContent);
        if (!isNaN(value) && value >= 1000) {
            stat.textContent = formatNumber(value);
        }
    });
    
    // --- TOOLTIPS INFORMATIVOS ---
    statCards.forEach(card => {
        const title = card.querySelector('.stat-card-title').textContent;
        card.setAttribute('title', `Ver detalles de ${title}`);
    });
    
    // --- ANIMACIÓN DE LOS ICONOS ---
    const cardIcons = document.querySelectorAll('.card-icon');
    cardIcons.forEach((icon, index) => {
        setTimeout(() => {
            icon.style.transition = 'all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
            icon.style.transform = 'scale(1.2)';
            setTimeout(() => {
                icon.style.transform = 'scale(1)';
            }, 300);
        }, 500 + (index * 100));
    });
    
    console.log('📊 Dashboard Admin inicializado correctamente');
});

// Agregar estilos para la animación ripple
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);