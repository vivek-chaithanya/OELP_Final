from .base import *
import os

# Use SQLite for fast, self-contained CI tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}

DEBUG = False
ALLOWED_HOSTS = ["*"]

# Minimal installed apps for tests inherit from base; CI-safe adjustments go here if needed

# Use local memory cache to avoid Redis dependency in CI
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-test-cache',
    }
}

# Email to console to avoid external services
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Auth model setting (keep consistent with dev/prod)
AUTH_USER_MODEL = 'accounts.CustomUser'

# JWT settings (keep simple/defaults during tests)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# Disable FCM/external keys in tests
FCM_DJANGO_SETTINGS = {
    'FCM_SERVER_KEY': 'test-key',
}

