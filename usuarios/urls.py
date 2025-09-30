# usuarios/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views # <-- Importante importar las vistas de auth
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # --- INICIO: BLOQUE PARA RECUPERAR CONTRASEÑA ---
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='usuarios/password_reset_form.html'), 
         name='password_reset'),
         
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), 
         name='password_reset_done'),
         
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'), 
         name='password_reset_confirm'),
         
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'), 
         name='password_reset_complete'),
    # --- FIN: BLOQUE PARA RECUPERAR CONTRASEÑA ---

    path('login/redirect/', views.login_redirect_view, name='login_redirect'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
]