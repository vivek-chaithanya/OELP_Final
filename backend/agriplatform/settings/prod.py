from .base import *
import os
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Ensure a secure secret key is used in production
if os.getenv("SECRET_KEY"):
    SECRET_KEY = os.getenv("SECRET_KEY")

INSTALLED_APPS += [
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf-spectacular',
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

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if os.getenv("CORS_ALLOWED_ORIGINS") else ["*"]

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

DATABASES = {
    'default': dj_database_url.parse(os.environ['DATABASE_URL'])
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', ''),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

FCM_DJANGO_SETTINGS = {
    'FCM_SERVER_KEY': os.getenv('FCM_SERVER_KEY', ''),
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.sendgrid.net')
EMAIL_HOST_USER = os.getenv('SENDGRID_USERNAME', 'apikey')
EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_API_KEY', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True


FRONTEND_DIR = os.path.join(BASE_DIR, "static")  # backend/agriplatform/static

STATIC_URL = "/static/"
STATICFILES_DIRS = [FRONTEND_DIR]

# Serve frontend index.html for catch-all routes
TEMPLATES[0]['DIRS'] = [FRONTEND_DIR]