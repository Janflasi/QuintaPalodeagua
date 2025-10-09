from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importa las vistas directamente si las usas aquí
from reservas import views as reservas_views
from usuarios import views as usuarios_views
from galeria import views as galeria_views

panel_control_patterns = [
    path('', reservas_views.dashboard_admin, name='dashboard_admin'),
    
    # Rutas de Usuarios
    path('usuarios/', usuarios_views.lista_usuarios_admin, name='lista_usuarios_admin'),
    path('usuarios/crear/', usuarios_views.crear_usuario_admin, name='crear_usuario_admin'),
    path('usuarios/toggle-active/<int:user_id>/', usuarios_views.activar_desactivar_usuario, name='toggle_usuario_active'),
    
    # Rutas de Reservas
    path('reservas/', reservas_views.lista_reservas_admin, name='lista_reservas_admin'),
    path('reservas/actualizar-estado/<int:reserva_id>/', reservas_views.actualizar_estado_reserva, name='actualizar_estado_reserva'),
    path('reservas/editar/<int:reserva_id>/', reservas_views.editar_reserva_admin, name='editar_reserva_admin'),
    
    # Rutas de Galería
    path('galeria/', galeria_views.gestionar_galeria_admin, name='gestionar_galeria_admin'),
    path('galeria/eliminar/<int:foto_id>/', galeria_views.eliminar_foto_admin, name='eliminar_foto_admin'),

    # Rutas de Reseñas
    path('resenas/', reservas_views.gestionar_resenas_admin, name='gestionar_resenas_admin'),
    path('resenas/aprobar/<int:resena_id>/', reservas_views.aprobar_resena_admin, name='aprobar_resena_admin'),
    path('resenas/eliminar/<int:resena_id>/', reservas_views.eliminar_resena_admin, name='eliminar_resena_admin'),

    # --- LÍNEA CORREGIDA AQUÍ ---
    path('contabilidad/', include('contabilidad.urls', namespace='contabilidad')),
]

urlpatterns = [
    path('super-admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # Mis Apps
    path('', include('core.urls')),
    path('galeria/', include('galeria.urls')),
    path('cuentas/', include('usuarios.urls')),
    path('reservas/', include('reservas.urls')),
    path('notificaciones/', include('notificaciones.urls')),

    # Panel de Control
    path('panel-control/', include(panel_control_patterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)