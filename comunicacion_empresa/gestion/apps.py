# gestion/apps.py
from django.apps import AppConfig

class GestionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion'

    def ready(self):
        import gestion.signals  # Importa las señales al iniciar la app