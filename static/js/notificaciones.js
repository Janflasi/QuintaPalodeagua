// static/js/notificaciones.js

document.addEventListener('DOMContentLoaded', function() {
    const notificationBell = document.getElementById('notification-bell');
    if (!notificationBell) return; // Si no existe la campana, no hacer nada

    const countBadge = document.getElementById('notification-count');
    const notificationList = document.getElementById('notification-list');
    const verNotificacionesUrl = '/notificaciones/ver/'; // URL que creamos en Django

    function fetchNotifications() {
        fetch(verNotificacionesUrl)
            .then(response => response.json())
            .then(data => {
                // Actualizar el contador
                if (data.count > 0) {
                    countBadge.textContent = data.count;
                    countBadge.style.display = 'inline';
                } else {
                    countBadge.style.display = 'none';
                }

                // Actualizar la lista desplegable
                if (data.notificaciones.length > 0) {
                    notificationList.innerHTML = ''; // Limpiar la lista
                    data.notificaciones.forEach(notif => {
                        const listItem = document.createElement('li');
                        const link = document.createElement('a');
                        link.href = `/notificaciones/marcar-leida/${notif.id}/`;
                        link.className = 'dropdown-item';
                        link.innerHTML = `
                            <div class="fw-bold">${notif.mensaje}</div>
                            <div class="small text-muted">${notif.fecha}</div>
                        `;
                        listItem.appendChild(link);
                        notificationList.appendChild(listItem);
                    });
                } else {
                    notificationList.innerHTML = '<li><a class="dropdown-item text-center" href="#">No hay notificaciones nuevas.</a></li>';
                }
            })
            .catch(error => console.error('Error al cargar notificaciones:', error));
    }

    // Cargar notificaciones al iniciar la página
    fetchNotifications();

    // Cargar notificaciones periódicamente (cada 15 segundos)
    setInterval(fetchNotifications, 15000);
});