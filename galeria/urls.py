# galeria/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URL pública (para visitantes)
    path('', views.galeria, name='galeria'),
    
    # URL para la galería DENTRO del panel de usuario
    path('panel/', views.galeria_panel_usuario, name='galeria_panel'),

    # URLS para el panel de admin (estas no cambian)
    path('panel-control/', views.gestionar_galeria_admin, name='gestionar_galeria_admin'),
    path('panel-control/eliminar/<int:foto_id>/', views.eliminar_foto_admin, name='eliminar_foto_admin'),
]