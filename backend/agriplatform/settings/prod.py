from .base import *
import os
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Ensure a secure secret key is used in production
if os.getenv("SECRET_KEY"):
    SECRET_KEY = os.getenv("SECRET_KEY")

# Override CORS settings for production
CORS_ALLOW_ALL_ORIGINS = True

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

# Override FCM settings for production
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