"""Configurações do WSGI para o projeoto DjangoSIGE."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangosige.configs.settings")

application = get_wsgi_application()
