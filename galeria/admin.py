from django.contrib import admin
from .models import Foto

# Registramos el modelo Foto para que aparezca en el admin
admin.site.register(Foto)