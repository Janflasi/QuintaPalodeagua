# contabilidad/urls.py
    
from django.urls import path
from . import views

# --- AÑADE ESTA LÍNEA ---
app_name = 'contabilidad'

urlpatterns = [
    path('', views.dashboard_contabilidad, name='dashboard_contabilidad'),
    path('inventario/', views.gestionar_inventario, name='gestionar_inventario'),
    path('movimiento/crear/<str:tipo_movimiento>/', views.crear_movimiento, name='crear_movimiento'),

]