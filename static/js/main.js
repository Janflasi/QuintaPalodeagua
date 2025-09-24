// static/js/main.js

// Espera a que todo el contenido del DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    
    // INICIALIZACIÓN DE FEATHER ICONS
    feather.replace();
    
    // --- NAVBAR SCROLL EFFECT ---
    const navbar = document.querySelector('.navbar-glass');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.backdropFilter = 'blur(20px)';
            navbar.style.boxShadow = '0 4px 20px rgba(212, 130, 90, 0.15)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.backdropFilter = 'blur(15px)';
            navbar.style.boxShadow = '0 4px 20px rgba(212, 130, 90, 0.1)';
        }
        
        // Ocultar/mostrar navbar en scroll
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        lastScrollTop = scrollTop;
    });

    // --- LÓGICA PARA EL CARRUSEL HERO ---
    const heroSliderElement = document.querySelector('.hero-slider');
    if (heroSliderElement) {
        const heroSlider = new Swiper('.hero-slider', {
            loop: true,
            autoplay: {
                delay: 6000, // Cambia de imagen cada 6 segundos
                disableOnInteraction: false,
                pauseOnMouseEnter: true,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
                dynamicBullets: true,
            },
            effect: 'fade',
            fadeEffect: {
                crossFade: true
            },
            speed: 1000, // Transición más suave
            // Agregar navegación con flechas si se desea
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
        });

        // Pausar autoplay cuando el usuario interactúa
        heroSliderElement.addEventListener('mouseenter', () => {
            heroSlider.autoplay.stop();
        });

        heroSliderElement.addEventListener('mouseleave', () => {
            heroSlider.autoplay.start();
        });
    }

    // --- ANIMACIONES DE ENTRADA SUAVES ---
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Aplicar animaciones a elementos con clase .animate-on-scroll
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        observer.observe(el);
    });

    // --- SMOOTH SCROLL PARA ENLACES INTERNOS ---
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const offsetTop = target.offsetTop - 80; // Compensar navbar fijo
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // --- LÓGICA PARA VALIDACIÓN DE CONTRASEÑAS EN REGISTRO ---
    const passwordField = document.getElementById('id_password1');
    const passwordConfirmField = document.getElementById('id_password2');

    if (passwordField && passwordConfirmField) {
        const messageDiv = document.createElement('div');
        messageDiv.id = 'password-message';
        messageDiv.classList.add('form-text', 'mt-2');
        messageDiv.style.fontSize = '0.9rem';
        messageDiv.style.fontWeight = '500';
        passwordConfirmField.parentNode.insertBefore(messageDiv, passwordConfirmField.nextSibling);

        function checkPasswords() {
            const pass1 = passwordField.value;
            const pass2 = passwordConfirmField.value;

            if (pass2 === '') {
                messageDiv.textContent = '';
                messageDiv.className = 'form-text mt-2';
                return;
            }

            if (pass1 === pass2) {
                messageDiv.innerHTML = '<span data-feather="check-circle" style="width: 16px; height: 16px;"></span> Las contraseñas coinciden';
                messageDiv.className = 'form-text mt-2 text-success d-flex align-items-center gap-1';
                feather.replace(); // Re-renderizar íconos
            } else {
                messageDiv.innerHTML = '<span data-feather="x-circle" style="width: 16px; height: 16px;"></span> Las contraseñas no coinciden';
                messageDiv.className = 'form-text mt-2 text-danger d-flex align-items-center gap-1';
                feather.replace(); // Re-renderizar íconos
            }
        }

        // Agregar efectos visuales a los campos de contraseña
        [passwordField, passwordConfirmField].forEach(field => {
            field.addEventListener('focus', function() {
                this.style.borderColor = 'var(--color-principal)';
                this.style.boxShadow = '0 0 0 0.2rem rgba(212, 130, 90, 0.25)';
            });

            field.addEventListener('blur', function() {
                this.style.borderColor = '';
                this.style.boxShadow = '';
            });
        });

        passwordField.addEventListener('keyup', checkPasswords);
        passwordConfirmField.addEventListener('keyup', checkPasswords);
    }

    // --- MEJORAR INTERACTIVIDAD DE BOTONES ---
    const buttons = document.querySelectorAll('.btn-principal');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });

        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });

        button.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(0)';
        });

        button.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-2px)';
        });
    });

    // --- ANIMACIÓN DE CARDS ---
    const cards = document.querySelectorAll('.card-custom');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 8px 30px rgba(212, 130, 90, 0.15)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 15px rgba(0, 0, 0, 0.05)';
        });
    });

    // --- LAZY LOADING PARA IMÁGENES ---
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // --- CERRAR ALERTS AUTOMÁTICAMENTE ---
    const alerts = document.querySelectorAll('.custom-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-10px)';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        }, 5000); // 5 segundos
    });

    // --- TOOLTIPS PARA ICONOS ---
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // --- EFECTO PARALLAX SUAVE PARA EL HERO ---
    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroContent.style.transform = `translateY(${rate}px)`;
        });
    }

    // --- VALIDACIÓN EN TIEMPO REAL PARA FORMULARIOS ---
    const formInputs = document.querySelectorAll('input, textarea, select');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.transition = 'all 0.3s ease';
            this.style.borderColor = 'var(--color-principal)';
            this.style.boxShadow = '0 0 0 0.2rem rgba(212, 130, 90, 0.25)';
        });

        input.addEventListener('blur', function() {
            this.style.borderColor = '';
            this.style.boxShadow = '';
        });

        // Agregar validación visual
        input.addEventListener('input', function() {
            if (this.checkValidity()) {
                this.style.borderColor = 'var(--color-success)';
            } else if (this.value.length > 0) {
                this.style.borderColor = '#F56565';
            }
        });
    });

    // --- NAVEGACIÓN SUAVE DEL MENÚ MÓVIL ---
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            
            // Animar las líneas del hamburger
            const spans = this.querySelectorAll('span');
            if (!isExpanded) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });

        // Cerrar menú al hacer clic en un enlace
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 992) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                        toggle: false
                    });
                    bsCollapse.hide();
                    
                    // Resetear hamburger
                    const spans = navbarToggler.querySelectorAll('span');
                    spans[0].style.transform = 'none';
                    spans[1].style.opacity = '1';
                    spans[2].style.transform = 'none';
                }
            });
        });
    }

    // --- PRELOADER SIMPLE ---
    window.addEventListener('load', function() {
        const preloader = document.querySelector('.preloader');
        if (preloader) {
            preloader.style.opacity = '0';
            setTimeout(() => {
                preloader.remove();
            }, 500);
        }
    });

    // --- CONTADOR DE CARACTERES PARA TEXTAREAS ---
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        const counter = document.createElement('div');
        counter.className = 'char-counter text-muted small text-end mt-1';
        counter.textContent = `0/${maxLength}`;
        textarea.parentNode.appendChild(counter);

        textarea.addEventListener('input', function() {
            const currentLength = this.value.length;
            counter.textContent = `${currentLength}/${maxLength}`;
            
            if (currentLength > maxLength * 0.9) {
                counter.style.color = '#F56565';
            } else {
                counter.style.color = 'var(--color-texto-light)';
            }
        });
    });

    // --- MODO OSCURO TOGGLE (OPCIONAL) ---
    const darkModeToggle = document.querySelector('#dark-mode-toggle');
    if (darkModeToggle) {
        const isDarkMode = localStorage.getItem('darkMode') === 'true';
        
        if (isDarkMode) {
            document.body.classList.add('dark-mode');
        }

        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDark);
        });
    }

    // --- EFECTO DE ESCRITURA PARA TÍTULOS PRINCIPALES ---
    function typeWriter(element, text, speed = 100) {
        let i = 0;
        element.innerHTML = '';
        
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        type();
    }

    // Aplicar efecto de escritura a elementos con clase .typewriter
    const typewriterElements = document.querySelectorAll('.typewriter');
    typewriterElements.forEach(element => {
        const text = element.textContent;
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    typeWriter(entry.target, text);
                    observer.unobserve(entry.target);
                }
            });
        });
        observer.observe(element);
    });

    console.log('🏡 Quinta Palo de Agua - Sistema inicializado correctamente');
});