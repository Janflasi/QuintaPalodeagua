# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('galeria/', include('galeria.urls')),
    path('cuentas/', include('usuarios.urls')), # <-- Agrega esta línea
    path('reservas/', include('reservas.urls')), # <-- Agrega esta línea

]

# Añade estas líneas al final para servir los archivos media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)