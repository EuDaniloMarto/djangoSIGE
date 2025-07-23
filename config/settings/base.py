""" Configurações base do projeto DjangoSIGE. """

from pathlib import Path

from decouple import config, Csv
from dj_database_url import parse as db_url


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "djangosige"

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = config("DEBUG", default=False, cast=bool)
SECRET_KEY = config("SECRET_KEY", default="alterar-em-producao")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=[], cast=Csv())

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    # Adicione aqui apps de terceiros que você possa usar (ex: crispy_forms, django-allauth)
]

LOCAL_APPS = [
    "djangosige.apps.base",
    "djangosige.apps.login",
    "djangosige.apps.cadastro",
    "djangosige.apps.vendas",
    "djangosige.apps.compras",
    "djangosige.apps.fiscal",
    "djangosige.apps.financeiro",
    "djangosige.apps.estoque",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE
# ------------------------------------------------------------------------------
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

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    "default": config(
        "DATABASE_URL",
        default="sqlite:///./db.sqlite3",
        cast=db_url
    ),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# PASSWORDS
# ------------------------------------------------------------------------------
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

# TEMPLATES
# ------------------------------------------------------------------------------
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

# SECURITY
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"  # Pode ser alterado por segurança em produção
ADMINS = [
    # ("Your Name", "your_email@example.com"),
]
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# FIXTURES
# ------------------------------------------------------------------------------
FIXTURE_DIRS = [str(APPS_DIR / "fixtures")]

# INTERNATIONALIZATION
# ------------------------------------------------------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "auth.User"  # Considere criar um CustomUser Model no futuro
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"
LOGIN_NOT_REQUIRED = (
    r"^/login/$",
    r"/login/esqueceu/",
    r"/login/trocarsenha/",
    r"/logout/",
)

# SESSIONS
# ------------------------------------------------------------------------------
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds (default Django)

# SITES
# ------------------------------------------------------------------------------
SITE_ID = 1  # Necessário se usar django.contrib.sites
