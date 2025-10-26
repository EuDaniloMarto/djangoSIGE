"""Configurações do projeto DjangoSIGE"""

from pathlib import Path

from decouple import Csv, config
from dj_database_url import parse as dburl

BASE_DIR = Path(__file__).resolve().parent.parent


# --- Geral
DEBUG = config("DEBUG", cast=bool)
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


TIME_ZONE = "America/Sao_Paulo"
LANGUAGE_CODE = "pt-br"
USE_I18N = True
USE_TZ = True

# -- Banco de dados
DATABASES = {"default": config("DATABASE_URL", cast=dburl)}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- URLS
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ---Apps
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

# --- Autenticação
AUTH_USER_MODEL = "auth.User"
# LOGIN_REDIRECT_URL = ""
# LOGIN_URL = ""
LOGIN_NOT_REQUIRED = (
    r"^/login/$",
    r"/login/esqueceu/",
    r"/login/trocarsenha/",
    r"/logout/",
)

# --- Senha
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

# --- Middleware
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

# --- Arquivos estáticos
# STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(BASE_DIR / "djangosige" / "static")]

# --- Arquivos de mídia
MEDIA_ROOT = str(BASE_DIR / "djangosige" / "media")
MEDIA_URL = "/media/"

# --- Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "djangosige" / "templates")],
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

# --- Fixtures
FIXTURE_DIRS = [str(BASE_DIR / "djangosige" / "fixtures")]

# --- Email

# --- Segurança
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
