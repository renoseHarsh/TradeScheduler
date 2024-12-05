from django.apps import AppConfig


class TradesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "trades"

    def ready(self):
        from .scheduler import start

        start()
