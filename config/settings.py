"""Configurações do projeto DjangoSIGE"""

from pathlib import Path

from decouple import Csv, config
from dj_database_url import parse as dburl

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
APPS_DIR = BASE_DIR / "djangosige"

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=[], cast=Csv())

# Geral
# ----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-DEBUG
DEBUG = config("DEBUG", default=True, cast=bool)
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-TIME_ZONE
TIME_ZONE = "America/Sao_Paulo"
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-LANGUAGE_CODE
LANGUAGE_CODE = "pt-br"
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-USE_I18N
USE_I18N = True
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-USE_L10N
USE_L10N = True
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-USE_TZ
USE_TZ = True

# Banco de dados
# ----------------------------------------------------------------------------
DATABASES = {"default": config("DATABASE_URL", default="sqlite:///./db.sqlite3", cast=dburl)}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-ROOT_URLCONF
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-WSGI_APPLICATION
WSGI_APPLICATION = "config.wsgi.application"

# Apps
# ----------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djangosige.apps.base",
    "djangosige.apps.login",
    "djangosige.apps.cadastro",
    "djangosige.apps.vendas",
    "djangosige.apps.compras",
    "djangosige.apps.fiscal",
    "djangosige.apps.financeiro",
    "djangosige.apps.estoque",
]

# Autenticação
# ----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
AUTH_USER_MODEL = "auth.User"

LOGIN_NOT_REQUIRED = (
    r"^/login/$",
    r"/login/esqueceu/",
    r"/login/trocarsenha/",
    r"/logout/",
)

# MIDDLEWARE
# ----------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djangosige.middleware.LoginRequiredMiddleware",
]

# Arquivos estáticos
# ----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/3.1/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = [str(APPS_DIR / "static")]

# Arquivos de mídia
# ----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#media-url
MEDIA_URL = "media/"
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-MEDIA_ROOT
MEDIA_ROOT = str(APPS_DIR / "media/")

# Templates
# ----------------------------------------------------------------------------
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
                "djangosige.apps.base.context_version.sige_version",
                "djangosige.apps.login.context_user.foto_usuario",
            ],
        },
    },
]

# Fixtures
# ----------------------------------------------------------------------------
FIXTURE_DIRS = [str(APPS_DIR / "fixtures")]

# Segurança
# ----------------------------------------------------------------------------
SECRET_KEY = config("SECRET_KEY", default="**uu$l52kin_*=53968cm5f#t2t8o$%b$-97senose6s!$dwcg")
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Email
# ----------------------------------------------------------------------------
