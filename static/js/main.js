// static/js/main.js

// Espera a que todo el contenido del DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    
    // INICIALIZACIÓN DE FEATHER ICONS
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // --- NAVBAR SCROLL EFFECT ---
    const navbar = document.querySelector('.navbar-glass');
    if (navbar) {
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
    }

    // --- LÓGICA PARA EL CARRUSEL HERO ---
    const heroSliderElement = document.querySelector('.hero-slider');
    if (heroSliderElement && typeof Swiper !== 'undefined') {
        const heroSlider = new Swiper('.hero-slider', {
            loop: true,
            autoplay: {
                delay: 6000,
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
            speed: 1000,
        });
    }

    // --- CARRUSEL DE TESTIMONIOS (MEJORADO) ---
    const testimonialsSliderElement = document.querySelector('.testimonials-slider');
    if (testimonialsSliderElement && typeof Swiper !== 'undefined') {
        const testimonialsSwiper = new Swiper('.testimonials-slider', {
            // Configuración de slides
            slidesPerView: 1,
            spaceBetween: 20,
            centeredSlides: false,
            
            // Loop y autoplay
            loop: true,
            loopAdditionalSlides: 2,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
                pauseOnMouseEnter: true,
            },
            
            // Navegación
            pagination: {
                el: '.testimonials-slider .swiper-pagination',
                clickable: true,
                dynamicBullets: false,
            },
            navigation: {
                nextEl: '.testimonials-slider .swiper-button-next',
                prevEl: '.testimonials-slider .swiper-button-prev',
            },
            
            // Responsive breakpoints (configuración mejorada)
            breakpoints: {
                // Móvil pequeño
                320: {
                    slidesPerView: 1,
                    spaceBetween: 15,
                },
                // Móvil mediano
                480: {
                    slidesPerView: 1,
                    spaceBetween: 20,
                },
                // Tablet pequeña
                640: {
                    slidesPerView: 1,
                    spaceBetween: 25,
                },
                // Tablet
                768: {
                    slidesPerView: 2,
                    spaceBetween: 25,
                },
                // Desktop pequeño
                1024: {
                    slidesPerView: 2,
                    spaceBetween: 30,
                },
                // Desktop mediano
                1200: {
                    slidesPerView: 3,
                    spaceBetween: 30,
                },
                // Desktop grande
                1400: {
                    slidesPerView: 3,
                    spaceBetween: 35,
                }
            },
            
            // Efectos y rendimiento
            speed: 600,
            effect: 'slide',
            
            // Interacción táctil
            touchEventsTarget: 'container',
            simulateTouch: true,
            grabCursor: true,
            touchRatio: 1,
            touchAngle: 45,
            
            // Prevenir clics durante transición
            preventClicks: true,
            preventClicksPropagation: true,
            
            // Accesibilidad
            watchSlidesProgress: true,
            watchSlidesVisibility: true,
            
            // Callback de inicialización
            on: {
                init: function() {
                    console.log('✅ Carrusel de testimonios inicializado');
                    // Ajustar altura inicial
                    this.update();
                },
                resize: function() {
                    // Actualizar al cambiar el tamaño de ventana
                    this.update();
                }
            }
        });
    }

    // --- ANIMACIONES DE ENTRADA SUAVES ---
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    if (animatedElements.length > 0) {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        animatedElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            observer.observe(el);
        });
    }
    
    // --- MANEJO DEL MENÚ MÓVIL (HAMBURGER) ---
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            const spans = this.querySelectorAll('span');
            
            if (isExpanded) {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            } else {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            }
        });
    }

    // --- PRELOADER SIMPLE ---
    window.addEventListener('load', function() {
        const preloader = document.querySelector('.preloader');
        if (preloader) {
            preloader.style.opacity = '0';
            setTimeout(() => {
                preloader.style.display = 'none';
            }, 500);
        }
    });

    console.log('🏡 Quinta Palo de Agua - Sistema inicializado correctamente');
});