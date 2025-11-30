from django.apps import AppConfig


class ProjectCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project_core'

    def ready(self):
        from . import signals  # Importa señales de disparador. 