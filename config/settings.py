"""Configurações do projeto djangosige"""

from pathlib import Path
from decouple import config, Csv
from dj_database_url import parse as dburl


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

APPS_DIR = BASE_DIR / "djangosige"


# --- Geral
# ----------------------------------------------------------------------------
DEBUG = config("DEBUG", default=False, cast=bool)
TIME_ZONE = "America/Sao_Paulo"
LANGUAGE_CODE = "pt-br"
USE_I18N = True
USE_TZ = True

# --- Banco de dados
# ----------------------------------------------------------------------------
DATABASES = {
    "default": config("DATABASE_URL", default="sqlite:///db.sqlite3", cast=dburl)
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- URLs
# ----------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", default=["127.0.0.1", "localhost", "0.0.0.0"], cast=Csv()
)
LOGIN_NOT_REQUIRED = (
    r"^/login/$",
    r"/login/esqueceu/",
    r"/login/trocarsenha/",
    r"/logout/",
)

# Apps
# ----------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "djangosige",
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
AUTH_USER_MODEL = "auth.User"
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

# Middleware
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
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_DIRS = [str(APPS_DIR / "static")]

# Arquivos de Mídia
# ----------------------------------------------------------------------------
MEDIA_URL = "media/"
MEDIA_ROOT = str(APPS_DIR / "media")

# Templates
# ----------------------------------------------------------------------------
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
                "djangosige.apps.base.context_version.sige_version",
                "djangosige.apps.login.context_user.foto_usuario",
            ],
        },
    },
]

# FIXTURES
# ----------------------------------------------------------------------------
# FIXTURE_DIRS = [str(APPS_DIR / "fixtures")]

# SECURITY
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
SECRET_KEY = config(
    "SECRET_KEY", default="wtyo881vmwl*!nwyeptchv_4!g(j8-)9_myvr2a7j=+kq7-&rn"
)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
