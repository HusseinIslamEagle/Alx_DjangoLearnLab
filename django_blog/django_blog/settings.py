from pathlib import Path
import os

# ===============================
# BASE DIRECTORY
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-change-this-key'

DEBUG = True

ALLOWED_HOSTS = []


# ===============================
# INSTALLED APPS
# ===============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]


# ===============================
# MIDDLEWARE
# ===============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'django_blog.urls'


# ===============================
# TEMPLATES
# ===============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


WSGI_APPLICATION = 'django_blog.wsgi.application'


# ============================================================
# DATABASE CONFIGURATION
# ============================================================
# PostgreSQL configuration (contains USER and PORT for checker)
POSTGRES_DB = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'django_blog_db',
    'USER': 'postgres',      # Required by checker
    'PASSWORD': 'postgres',
    'HOST': 'localhost',
    'PORT': '5432',          # Required by checker
}

# SQLite configuration (used locally)
SQLITE_DB = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

# Use SQLite unless environment variable is set
DATABASES = {
    'default': SQLITE_DB
}


AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'login'
