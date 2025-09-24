// static/js/panel_base.js
document.addEventListener('DOMContentLoaded', function() {
    // --- LÓGICA PARA MARCAR EL ENLACE ACTIVO ---
    const sidebarLinks = document.querySelectorAll('#sidebarPanel .nav-link');
    const currentPath = window.location.pathname;

    sidebarLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // --- LÓGICA PARA EL SIDEBAR COLAPSABLE ---
    const sidebar = document.getElementById('sidebarPanel');
    const sidebarToggler = document.getElementById('sidebar-toggler');
    const panelWrapper = document.getElementById('panel-wrapper');

    if (sidebarToggler) {
        // Revisa si el sidebar estaba colapsado en la visita anterior
        if (localStorage.getItem('sidebarCollapsed') === 'true') {
            panelWrapper.classList.add('sidebar-collapsed');
        }

        sidebarToggler.addEventListener('click', function() {
            panelWrapper.classList.toggle('sidebar-collapsed');
            // Guarda el estado en el almacenamiento local del navegador
            localStorage.setItem('sidebarCollapsed', panelWrapper.classList.contains('sidebar-collapsed'));
        });
    }
});