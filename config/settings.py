import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


# =============================================================================
# BASE CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "unsafe-development-key",
)

DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# =============================================================================
# ALLOWED HOSTS
# =============================================================================

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

# Railway automatically provides this when the service has a public domain.
railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")

if railway_domain:
    ALLOWED_HOSTS.append(
        railway_domain.strip()
    )

# Additional hosts can be supplied through Railway.
#
# Example:
# ALLOWED_HOSTS=example.com,www.example.com
#
extra_allowed_hosts = os.getenv(
    "ALLOWED_HOSTS",
    "",
)

if extra_allowed_hosts:
    ALLOWED_HOSTS.extend(
        host.strip()
        for host in extra_allowed_hosts.split(",")
        if host.strip()
    )

# Remove duplicates while preserving order.
ALLOWED_HOSTS = list(
    dict.fromkeys(ALLOWED_HOSTS)
)


# =============================================================================
# APPLICATIONS
# =============================================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",

    # Local
    "departments",
    "accounts",
    "request_management",
    "workflow",
    "notifications",
    "audit",
    "reports",
]


# =============================================================================
# MIDDLEWARE
# =============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise
    "whitenoise.middleware.WhiteNoiseMiddleware",

    # CORS
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


# =============================================================================
# TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# =============================================================================
# DATABASE
# =============================================================================
#
# LOCAL:
#   DATABASE_URL does not exist → SQLite
#
# RAILWAY:
#   DATABASE_URL exists → PostgreSQL
#
# =============================================================================

if os.getenv("DATABASE_URL"):

    import dj_database_url

    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

else:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# =============================================================================
# STATIC FILES
# =============================================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

# IMPORTANT:
# Use CompressedStaticFilesStorage instead of
# CompressedManifestStaticFilesStorage.
#
# This avoids manifest-related failures while the project is being deployed.
STORAGES = {
    "default": {
        "BACKEND": (
            "django.core.files.storage.FileSystemStorage"
        ),
    },

    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedStaticFilesStorage"
        ),
    },
}


# =============================================================================
# MEDIA FILES
# =============================================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =============================================================================
# EMAIL
# =============================================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)


# =============================================================================
# DJANGO REST FRAMEWORK
# =============================================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}


# =============================================================================
# CORS
# =============================================================================
#
# Local React:
#   http://localhost:5173
#
# Production React:
#   FRONTEND_URL=https://your-frontend.vercel.app
#
# =============================================================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

frontend_url = os.getenv(
    "FRONTEND_URL"
)

if frontend_url:
    frontend_url = frontend_url.rstrip("/")

    if frontend_url not in CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS.append(
            frontend_url
        )


# =============================================================================
# CSRF
# =============================================================================
#
# The production frontend must be trusted for CSRF-protected requests.
#
# The Railway backend itself does NOT need to be added here merely because
# Django admin is hosted on Railway. Same-origin admin requests are already
# trusted.
#
# =============================================================================

CSRF_TRUSTED_ORIGINS = []

if frontend_url:
    CSRF_TRUSTED_ORIGINS.append(
        frontend_url
    )


# =============================================================================
# PRODUCTION HTTPS / RAILWAY
# =============================================================================

if not DEBUG:

    # Railway terminates HTTPS at the proxy.
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    # Do not redirect HTTP ourselves because Railway handles
    # the external HTTPS connection.
    SECURE_SSL_REDIRECT = False

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# =============================================================================
# DEFAULT PRIMARY KEY
# =============================================================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)


# =============================================================================
# CUSTOM USER
# =============================================================================

AUTH_USER_MODEL = "accounts.User"


# =============================================================================
# JWT
# =============================================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=60
    ),

    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=1
    ),

    "ROTATE_REFRESH_TOKENS": True,

    "BLACKLIST_AFTER_ROTATION": True,
}