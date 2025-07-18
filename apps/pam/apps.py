from django.apps import AppConfig


class PamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pam'
    verbose_name = 'File Server Authentication'

    def ready(self):
        import pam.signals
