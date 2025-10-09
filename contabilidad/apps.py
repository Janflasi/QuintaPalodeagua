# contabilidad/apps.py

from django.apps import AppConfig

class ContabilidadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contabilidad'

    # --- AÑADE ESTA FUNCIÓN ---
    def ready(self):
        import contabilidad.signals