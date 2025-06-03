"""Configurações do projeto DjangoSIGE"""

from pathlib import Path

from decouple import Csv, config
from dj_database_url import parse as dburl

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

APPS_DIR = BASE_DIR / "djangosige"

# --- Geral ------------------------------------------------------------------
DEBUG = config("DEBUG", default=False, cast=bool)

TIME_ZONE = "America/Sao_Paulo"
LANGUAGE_CODE = "pt-br"
USE_I18N = True
USE_TZ = True

# --- Banco de dados ---------------------------------------------------------
DATABASES = {
    "default": config("DATABASE_URL", default="sqlite:///db.sqlite3", cast=dburl)
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- URLS -------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=[], cast=Csv())

# --- Apps -------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djangosige",
    "djangosige.base",
    "djangosige.login",
    "djangosige.cadastro",
    "djangosige.vendas",
    "djangosige.compras",
    "djangosige.fiscal",
    "djangosige.financeiro",
    "djangosige.estoque",
]

# --- Autenticação -----------------------------------------------------------
AUTH_USER_MODEL = "auth.User"
# LOGIN_REDIRECT_URL
# LOGIN_URL
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

# --- Middleware -------------------------------------------------------------
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

# --- Arquivos estáticos -----------------------------------------------------
STATIC_URL = "/static/"

# --- Arquivos de mídia ------------------------------------------------------
MEDIA_URL = "media/"
MEDIA_ROOT = str(APPS_DIR / "media")

# --- Templates --------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "djangosige.base.context_version.sige_version",
                "djangosige.login.context_user.foto_usuario",
            ],
        },
    },
]

# --- Segurança --------------------------------------------------------------
SECRET_KEY = config("SECRET_KEY", default="16&yg*=-du53b$7o&!t&v0mlnzdr=a_3rx7ke3t7ux)((o$n++")
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
