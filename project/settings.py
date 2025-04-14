import boto3
from botocore.auth import SigV4Auth

from pathlib import Path
import os
import sys
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1', 't')

print(">", os.getenv('PONG'))

USE_S3 = os.getenv('USE_S3', 'False').lower() in ('true', '1', 't')

# Configuración de App Runner
APP_RUNNER_SUBDOMAIN = os.getenv('APP_RUNNER_SUBDOMAIN')
APP_RUNNER_REGION = os.getenv('APP_RUNNER_REGION')
APP_RUNNER_DOMAIN = os.getenv('APP_RUNNER_DOMAIN')

# Construir el host completo de App Runner
APP_RUNNER_HOST = f"{APP_RUNNER_SUBDOMAIN}.{APP_RUNNER_REGION}.{APP_RUNNER_DOMAIN}" if all([APP_RUNNER_SUBDOMAIN, APP_RUNNER_REGION, APP_RUNNER_DOMAIN]) else None

# Configurar ALLOWED_HOSTS
ALLOWED_HOSTS = [f".{APP_RUNNER_DOMAIN}"] if APP_RUNNER_DOMAIN else ['localhost', '127.0.0.1']

# Construir CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS = [f"https://{APP_RUNNER_HOST}"] if APP_RUNNER_HOST else []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

print(">", os.getenv('DATABASE_URL'))
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'), conn_max_age=600, conn_health_checks=True)

}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-AR'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

S3_REGION = os.getenv('S3_REGION', 'us-east-1')

if USE_S3:
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    AWS_S3_SIGNATURE_VERSION = 's3v4'

    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_VERIFY = True
    AWS_LOCATION_STATIC = 'static'  # Default location for static files
    AWS_LOCATION_MEDIA = 'media'

    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
            'OPTIONS': {
                'bucket_name': S3_BUCKET_NAME,
                'location': AWS_LOCATION_MEDIA,
                'file_overwrite': AWS_S3_FILE_OVERWRITE,
                'signature_version': AWS_S3_SIGNATURE_VERSION,
                'addressing_style': 'virtual',
                'session': boto3.session.Session(region_name=S3_REGION),
            },


        },
        'staticfiles': {
            'BACKEND': 'storages.backends.s3boto3.S3StaticStorage',
            'OPTIONS': {
                'bucket_name': S3_BUCKET_NAME,
                'location': AWS_LOCATION_STATIC,
                'file_overwrite': False,
                'signature_version': AWS_S3_SIGNATURE_VERSION,
                'addressing_style': 'virtual',
            },
        },

    }

    STATIC_URL = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{AWS_LOCATION_STATIC}/"  # Updated this line
    MEDIA_URL = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{AWS_LOCATION_MEDIA}/"  # Updated this line
else:

    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
         'core': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}
