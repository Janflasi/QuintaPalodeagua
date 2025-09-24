# core/urls.py (archivo nuevo)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # La '' significa la raíz (página de inicio)
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
]