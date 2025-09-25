from .base import *
import os
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ["*"]

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

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


