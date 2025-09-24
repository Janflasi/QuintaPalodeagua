# usuarios/urls.py
from django.urls import path
# Quitamos LoginView porque ya no la usaremos directamente
from django.contrib.auth.views import LogoutView 
from . import views # Importamos nuestras vistas

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    
    # --- CAMBIAMOS ESTA LÍNEA ---
    path('login/', views.login_inteligente, name='login'), # Ahora apunta a nuestra vista
    
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
]