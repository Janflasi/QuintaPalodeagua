# galeria/urls.py (archivo nuevo)
from django.urls import path
from . import views

urlpatterns = [
    # Cuando alguien visite /galeria/, se activará la vista 'galeria'
    path('', views.galeria, name='galeria'),
]