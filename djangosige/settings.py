"""Configurações do projeto DjangoSIGE"""

from pathlib import Path  # noqa: I001

from decouple import Csv, config
from dj_database_url import parse as dburl

# Configurações de Paths
# Acessa a pasta raiz do projeto Django (onde fica manage.py)
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# project_name/
APPS_DIR = BASE_DIR / "djangosige"


# GERAL
# ------------------------------------------------------------------------------
DEBUG = config("DEBUG", cast=bool)
TIME_ZONE = "America/Sao_Paulo"
LANGUAGE_CODE = "pt-br"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True


# URLs
# ------------------------------------------------------------------------------
ROOT_URLCONF = "djangosige.urls"
WSGI_APPLICATION = "djangosige.wsgi.application"


# Segurança
# ------------------------------------------------------------------------------
SECRET_KEY = config("SECRET_KEY")
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


# Banco de dados
# ------------------------------------------------------------------------------
DATABASES = {"default": config("DATABASE_URL", cast=dburl)}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Aplicações
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.sites",
    "crispy_forms",
    "crispy_bootstrap5",
]
if DEBUG:
    INSTALLED_APPS += [
        "whitenoise.runserver_nostatic",
        "debug_toolbar",
        "django_extensions",
    ]

INSTALLED_APPS += [
    "djangosige.apps.base.apps.BaseConfig",
    "djangosige.apps.login.apps.LoginConfig",
    "djangosige.apps.cadastro.apps.CadastroConfig",
    "djangosige.apps.vendas.apps.VendasConfig",
    "djangosige.apps.compras.apps.ComprasConfig",
    "djangosige.apps.fiscal.apps.FiscalConfig",
    "djangosige.apps.financeiro.apps.FinanceiroConfig",
    "djangosige.apps.estoque.apps.EstoqueConfig",
]


# Autenticação e Sessão
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "auth.User"
# LOGIN_REDIRECT_URL = "users:redirect"  # noqa: ERA001
# LOGIN_URL = "account_login"  # noqa: ERA001

# A lista de URLs que não requerem login deve ser tratada no middleware.
# Mantendo o formato original como uma tupla para o middleware
LOGIN_NOT_REQUIRED = (
    r"^/login/$",
    r"/login/esqueceu/",
    r"/login/trocarsenha/",
    r"/logout/",
)


# Validação de Senha
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},  # noqa: E501
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Middleware
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djangosige.middleware.LoginRequiredMiddleware",
]

if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

# Static/Media
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = str(APPS_DIR / "staticfiles")

# Arquivos estáticos em desenvolvimento
STATICFILES_DIRS = [
    str(APPS_DIR / "static"),
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Configuração de Media Files
MEDIA_URL = "/media/"
MEDIA_ROOT = str(APPS_DIR / "media")


# Templates
# ------------------------------------------------------------------------------
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
    }
]

CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": [
            "debug_toolbar.panels.redirects.RedirectsPanel",
            # Disable profiling panel due to an issue with Python 3.12+:
            # https://github.com/jazzband/django-debug-toolbar/issues/1875
            "debug_toolbar.panels.profiling.ProfilingPanel",
        ],
        "SHOW_TEMPLATE_CONTEXT": True,
    }
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# Segurança
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

# Email (Configurações comuns)
# ------------------------------------------------------------------------------
# Padrão para SMTP, mas o Cookiecutter Django geralmente usa django-anymail
# e Mailgun/Sendgrid. Simplificado para o seu padrão.
EMAIL_BACKEND = config(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="webmaster@localhost")


# Fixtures
# ------------------------------------------------------------------------------
FIXTURE_DIRS = [
    str(APPS_DIR / "fixtures"),
]
