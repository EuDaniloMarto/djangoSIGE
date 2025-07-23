""" Configurações de produção para o DjangoSIGE. """

from .base import *  # noqa: F403, F401
from .base import DATABASES
from decouple import config, Csv
from dj_database_url import parse as db_url

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = False  # Sempre False em produção!

SECRET_KEY = config("DJANGO_SECRET_KEY")  # Chave secreta deve vir OBRIGATORIAMENTE de variável de ambiente em produção!

# Em produção, Allowed_Hosts deve ser explicitamente definido com os domínios reais
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# DATABASES
# ------------------------------------------------------------------------------
# A URL do banco de dados deve vir de uma variável de ambiente em produção.
DATABASES["default"] = config("DATABASE_URL", cast=db_url)
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # Já está em base, mas reforça

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL", default="redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,  # Para evitar que falhas no cache derrubem a aplicação
        },
    }
}

# SECURITY
# ------------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# EMAIL
# ------------------------------------------------------------------------------
# Configurações de e-mail específicas para produção (servidor SMTP real)
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="DjangoSIGE <noreply@example.com>")
SERVER_EMAIL = DEFAULT_FROM_EMAIL  # E-mail para erros do servidor

# ADMIN
# ------------------------------------------------------------------------------
# URL do admin customizada para segurança
ADMIN_URL = config("DJANGO_ADMIN_URL", default="admin/")  # Mude isso em produção!

# LOGGING
# ------------------------------------------------------------------------------
# Configurações de log mais robustas para produção
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
