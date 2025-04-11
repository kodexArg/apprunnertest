"""
Configuración de Django para el proyecto.

Variables de entorno requeridas:
DJANGO_SECRET_KEY: Clave secreta para firmar datos criptográficos (ej: 'django-insecure-1234567890abcdefghijklmnopqrstuvwxyz')
DJANGO_DEBUG: Indica si el modo de depuración está activado (ej: 'False' para producción, 'True' para desarrollo)

# Configuración de App Runner
APP_RUNNER_SUBDOMAIN: Subdominio asignado por App Runner (ej: 'nqya523khr')
APP_RUNNER_REGION: Región de App Runner (ej: 'us-east-1')
APP_RUNNER_DOMAIN: Dominio base de App Runner (ej: 'awsapprunner.com')

# Configuración de base de datos
DATABASE_URL o WELPDESK_DB_CONNECTOR: URL de conexión a la base de datos (ej: 'postgres://usuario:contraseña@host:5432/nombre_db')

# Configuración de AWS S3
AWS_STORAGE_BUCKET_NAME: Nombre del bucket de S3 para almacenamiento (ej: 'alvs-virginia-s3')
AWS_REGION_NAME: Región de AWS para S3 (ej: 'us-east-1')
AWS_S3_CUSTOM_DOMAIN: Dominio personalizado para CloudFront, opcional (ej: 'd1234567890.cloudfront.net')
"""

from pathlib import Path
import os
import sys
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1', 't')

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

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', os.getenv('WELPDESK_DB_CONNECTOR')),
        conn_max_age=600,
        conn_health_checks=True
    )
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

if not DEBUG:
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')

    AWS_ACCESS_KEY_ID = None  # Use instance role
    AWS_SECRET_ACCESS_KEY = None  # Use instance role

    AWS_DEFAULT_ACL = None  # Use bucket policy
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_VERIFY = True

    AWS_LOCATION_STATIC = 'static'
    AWS_LOCATION_MEDIA = 'media'

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "location": AWS_LOCATION_MEDIA,
                "file_overwrite": AWS_S3_FILE_OVERWRITE,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
            "OPTIONS": {
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "location": AWS_LOCATION_STATIC,
                "file_overwrite": True,
            },
        },
    }

    if AWS_S3_CUSTOM_DOMAIN:
        STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION_STATIC}/"
        MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION_MEDIA}/"
    else:
        STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{AWS_LOCATION_STATIC}/"
        MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{AWS_LOCATION_MEDIA}/"
else:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

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
