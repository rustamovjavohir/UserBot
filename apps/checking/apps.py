from django.apps import AppConfig


class CheckingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.checking'

    def ready(self):
        import apps.checking.signals
