"""
Local development settings for {{ cookiecutter.project_name }}.
"""

from .base import *  # noqa: F401, F403, A004

DEBUG = True

INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
    "django_extensions",
]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

# Allow all origins in local development
CORS_ALLOW_ALL_ORIGINS = True

# Email: console backend (prints to stdout)
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")  # noqa: F405

# Debug toolbar
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# Simplify password validation in local dev
AUTH_PASSWORD_VALIDATORS = []

# Cache: use local memory in development
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
}

# Disable CORS restrictions in local dev
CORS_ALLOW_CREDENTIALS = True  # noqa: F811
