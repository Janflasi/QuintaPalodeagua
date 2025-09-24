# usuarios/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    
    # URL para Iniciar Sesión
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    
    # URL para Cerrar Sesión
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
]