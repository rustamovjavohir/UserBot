from django.apps import AppConfig


class StaffConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.staff'
    verbose_name = "Зарплата"

    def ready(self):
        pass
# pass