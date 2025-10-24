import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-desarrollo-local-solo-cambiar-en-produccion')

DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'prediction_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'titanic_predictor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'titanic_predictor.wsgi.application'

# DATABASE CONFIGURACIÓN SIMPLIFICADA
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración para Railway (sin dj-database-url)
if 'DATABASE_URL' in os.environ:
    db_url = os.environ['DATABASE_URL']
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    # Configuración manual de PostgreSQL
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE', 'railway'),
        'USER': os.environ.get('PGUSER', 'postgres'),
        'PASSWORD': os.environ.get('PGPASSWORD', ''),
        'HOST': os.environ.get('PGHOST', 'localhost'),
        'PORT': os.environ.get('PGPORT', '5432'),
    }

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SAMESITE = 'Lax'

# Agrega tu dominio de Railway a ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'simulationstatus-production.up.railway.app',
    'localhost',
    '127.0.0.1',
]

# Configura CSRF_TRUSTED_ORIGINS para HTTPS
CSRF_TRUSTED_ORIGINS = [
    'https://simulationstatus-production.up.railway.app',
    'https://*.railway.app',
]
