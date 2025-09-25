# reservas/urls.py (archivo nuevo)
from django.urls import path
from . import views

urlpatterns = [
    path('panel/', views.panel_usuario, name='panel_usuario'),
    path('crear/', views.crear_reserva, name='crear_reserva'), # <-- Añade esta línea
     path('disponibilidad/', views.ver_disponibilidad, name='ver_disponibilidad'), # <-- Añade esta
]