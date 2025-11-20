from django.apps import AppConfig


class Cadastros(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "djangosige.cadastros"

    def ready(self):
        import djangosige.cadastros.signals
