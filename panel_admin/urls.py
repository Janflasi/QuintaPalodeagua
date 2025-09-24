# panel_admin/urls.py (archivo nuevo)
from django.urls import path
from . import views

urlpatterns = [
   path('', views.dashboard, name='admin_dashboard'),
    path('reservas/', views.gestionar_reservas, name='admin_gestionar_reservas'), # <-- Añade esta línea
     # --- NUEVAS RUTAS ---
    path('reservas/<int:reserva_id>/confirmar/', views.confirmar_reserva, name='admin_confirmar_reserva'),
    path('reservas/<int:reserva_id>/cancelar/', views.cancelar_reserva, name='admin_cancelar_reserva'),
    path('usuarios/', views.ver_usuarios, name='admin_ver_usuarios'),
]