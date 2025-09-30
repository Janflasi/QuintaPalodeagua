# notificaciones/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('ver/', views.ver_notificaciones, name='ver_notificaciones'),
    path('marcar-leida/<int:notificacion_id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
]