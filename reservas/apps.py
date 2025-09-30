# reservas/apps.py

from django.apps import AppConfig

class ReservasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservas'

    def ready(self):
        # Importa las señales para que se registren cuando la app esté lista
        import reservas.signals