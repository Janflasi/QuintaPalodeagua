# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importamos las vistas de las apps que necesitamos para el panel
from reservas import views as reservas_views
from usuarios import views as usuarios_views
from galeria import views as galeria_views # <-- Añadimos la importación de galería

# --- GRUPO DE URLS PARA EL PANEL DE CONTROL ---
panel_control_patterns = [
    path('', reservas_views.dashboard_admin, name='dashboard_admin'),
    
    # URLs de gestión de usuarios
    path('usuarios/', usuarios_views.lista_usuarios_admin, name='lista_usuarios_admin'),
    path('usuarios/<int:user_id>/toggle-active/', usuarios_views.activar_desactivar_usuario, name='toggle_usuario_active'),
    
    # URLs de gestión de reservas
    path('reservas/', reservas_views.lista_reservas_admin, name='lista_reservas_admin'),
    path('reservas/<int:reserva_id>/actualizar/', reservas_views.actualizar_estado_reserva, name='actualizar_estado_reserva'),
    path('reservas/<int:reserva_id>/editar/', reservas_views.editar_reserva_admin, name='editar_reserva_admin'),
    
    # URLs de gestión de galería
    path('galeria/', galeria_views.gestionar_galeria_admin, name='gestionar_galeria_admin'),
    path('galeria/eliminar/<int:foto_id>/', galeria_views.eliminar_foto_admin, name='eliminar_foto_admin'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs del sitio principal (públicas y de usuario normal)
    path('', include('core.urls')),
    path('galeria/', include('galeria.urls')),
    path('cuentas/', include('usuarios.urls')),
    path('reservas/', include('reservas.urls')),
    path('notificaciones/', include('notificaciones.urls')), # <-- AÑADE ESTA LÍNEA

    # --- RUTA PRINCIPAL PARA EL PANEL DE CONTROL ---
    path('panel-control/', include(panel_control_patterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)