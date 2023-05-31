from pathlib import Path
import os
import pymysql
import sys
import dj_database_url
import environ
from django.core.management.utils import get_random_secret_key

pymysql.install_as_MySQLdb()
env = environ.Env()
environ.Env.read_env()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-prrh+(pacdr5xg^otx%_pfvnp%=scus3-k@4#br3i60&laa!b%'
# SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# DEBUG = True
DEBUG = os.getenv("DEBUG", "False") == "True"
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

# ALLOWED_HOSTS = ['*','127.0.0.1','stellar-dynamics.com','www.stellar-dynamics.com','159.65.8.105']
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'Line',
    'User',
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

ROOT_URLCONF = 'QAS.urls'

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

WSGI_APPLICATION = 'QAS.wsgi.application'

## Production Database
# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.mysql',
#          'NAME': 'chatbot',
#          'USER': 'sammy',
#          'PASSWORD': '@Wing5Game',
#          'HOST': '159.65.8.105',
#      }
# }

# Local Database
# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.mysql',
#          'NAME': 'qas',
#          'USER': 'root',
#          'PASSWORD': '',
#          'HOST': 'localhost',
#      }
# }


if DEVELOPMENT_MODE is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'qas',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'qas',
            'USER': 'root',
            'PASSWORD': '@Blacky2000pi',
            'HOST': 'localhost',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/register_check/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
#STATICFILES_DIRS = ( os.path.join('static'), )
# STATICFILES_DIRS = [
#    BASE_DIR / 'static'
# ]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = ''
