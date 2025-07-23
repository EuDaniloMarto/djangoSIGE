""" Configurações de desenvolvimento local para o DjangoSIGE. """

from .base import *  # noqa: F403, F401
from .base import LOGGING
from decouple import config

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True  # Garante DEBUG True em desenvolvimento
# Em dev, pode usar um valor mais simples, mas idealmente ainda via variável de ambiente.
SECRET_KEY = config("DJANGO_SECRET_KEY", default="your-dev-secret-key-that-is-not-for-prod")
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config("EMAIL_PORT", default=1025, cast=int)  # Porta comum para Mailhog/Mailpit
# O restante das configurações de e-mail podem ser mantidas no base ou ajustadas aqui se necessário.

# White-listed IPs (opcional, para debug_toolbar)
INTERNAL_IPS = [
    "127.0.0.1",
]

# django-debug-toolbar
# ------------------------------------------------------------------------------
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
# DEBUG_TOOLBAR_CONFIG = {
#     "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
#     "SHOW_TOOLBAR_CALLBACK": lambda request: True, # Sempre mostra a toolbar em dev
# }

# LOGGING
# ------------------------------------------------------------------------------
LOGGING["root"]["level"] = "DEBUG"  # Nível de log mais verboso em dev
