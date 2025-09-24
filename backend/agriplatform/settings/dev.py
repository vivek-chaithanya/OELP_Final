from .base import *
import os
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'fcm_django',
    'accounts',
    'core',
    'subscriptions',
    'notifications',
    'analytics',
    'payments',
    'api',
]

MIDDLEWARE.insert(1, 'corsheaders.middleware.CorsMiddleware')

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Agri Platform API',
    'DESCRIPTION': 'OELP Farming Platform API',
    'VERSION': '1.0.0',
}

AUTH_USER_MODEL = 'accounts.CustomUser'

if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(os.environ['DATABASE_URL'])
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'agriplatform',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

FCM_DJANGO_SETTINGS = {
    'FCM_SERVER_KEY': 'REPLACE_ME',
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


