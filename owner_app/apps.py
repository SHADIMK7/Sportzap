from django.apps import AppConfig

class OwnerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'owner_app'

    def ready(self):
        import owner_app.signals