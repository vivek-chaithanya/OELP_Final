from .dev import *
import os

DEBUG = False
ALLOWED_HOSTS = ["*"]

# Use local memory cache to avoid Redis dependency in CI
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-test-cache',
    }
}

# Email to console to avoid external services
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# JWT / DRF settings for CI
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # AllowAny for CI
    ),
}

# Database configuration for CI (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'agriplatform'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Faster password hashing for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable FCM/external keys in tests
FCM_DJANGO_SETTINGS = {
    'FCM_SERVER_KEY': 'test-key',
}
