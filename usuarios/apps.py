# usuarios/apps.py

from django.apps import AppConfig

class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    # Este método se asegura de que se cargue el archivo models.py,
    # que es donde están nuestras señales.
    def ready(self):
        from . import models