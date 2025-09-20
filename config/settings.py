"""Configurações do projeto DjangoSIGE"""

from pathlib import Path

from decouple import Csv, config
from dj_database_url import parse as dburl

BASE_DIR = Path(__file__).resolve().parent.parent

APPS_DIR = BASE_DIR / "djangosige"

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# DEBUG
DEBUG = config("DEBUG", cast=bool)

# DATABASES
DATABASES = {"default": config("DATABASE_URL", cast=dburl)}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# EMAIL
EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_SSL = config("EMAIL_USE_SSL")
EMAIL_USE_TLS = config("EMAIL_USE_TLS")

# Globalization
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# HTTP
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
WSGI_APPLICATION = "config.wsgi.application"

# Models
FIXTURE_DIRS = [str(APPS_DIR / "fixtures")]
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "djangosige.apps.base",
    # "djangosige.apps.login",
    # "djangosige.apps.cadastro",
    # "djangosige.apps.vendas",
    # "djangosige.apps.compras",
    # "djangosige.apps.fiscal",
    # "djangosige.apps.financeiro",
    # "djangosige.apps.estoque",
]

# Security
SECRET_KEY = config("SECRET_KEY")

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # "djangosige.apps.base.context_version.sige_version",
                # "djangosige.apps.login.context_user.foto_usuario",
            ],
        },
    },
]

# URL
ROOT_URLCONF = "config.urls"

# Auth
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
LOGIN_NOT_REQUIRED = (
    r"^/login/$",
    r"/login/esqueceu/",
    r"/login/trocarsenha/",
    r"/logout/",
)

# Sessions

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]

# File Uploads
MEDIA_URL = "media/"
MEDIA_ROOT = APPS_DIR / "media"
