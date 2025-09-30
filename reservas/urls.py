from django.urls import path
from . import views

urlpatterns = [
    # --- URLS PARA USUARIOS REGULARES ---
    path('panel/', views.panel_usuario, name='panel_usuario'),
    path('crear/', views.crear_reserva, name='crear_reserva'),
    
    # Rutas para el calendario de disponibilidad
    # NOTA: La primera ruta es para el mes actual y tiene el nombre 'ver_disponibilidad_actual'
    path('disponibilidad/', views.ver_disponibilidad, name='ver_disponibilidad_actual'),
    
    # NOTA: La segunda ruta es para navegar y tiene el nombre 'ver_disponibilidad'
    path('disponibilidad/<int:year>/<int:month>/', views.ver_disponibilidad, name='ver_disponibilidad'),
    
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva_usuario, name='cancelar_reserva_usuario'),
]