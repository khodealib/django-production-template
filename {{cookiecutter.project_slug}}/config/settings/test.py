"""
Test settings for {{ cookiecutter.project_name }}.
"""

from .base import *  # noqa: F401, F403, A004

DEBUG = False

# Use fast password hasher for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Email: in-memory backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Disable CORS in tests
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS: list[str] = []  # noqa: F405

# Disable HSTS in tests
SECURE_HSTS_SECONDS = 0
SECURE_SSL_REDIRECT = False

# Faster tests
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # noqa: F811

# Logging: minimal in tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "handlers": ["null"],
        "level": "CRITICAL",
    },
}
