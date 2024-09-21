from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import os

#loads a .env file. There is no .env file ?
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# used to provide cryptographic signing, and should be set to a unique, unpredictable value.
# read more at https://docs.djangoproject.com/en/5.1/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = 'django-insecure-n!-hggli0wd1(2=4!gsrbpt3=px4xxbed$ocvvw2v2+3cq+xz*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
INTERNAL_IPS = [
    "127.0.0.1",
]
#list of allowed hosts that can perform requests to django
#matches with host headers in requests
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

#configures default authentication and permissions
#users need to authenticate with session or token to use any endpoint
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        'rest_framework.authentication.TokenAuthentication',
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    #generates API documentation based on the OpenAPI 3.0 standard.
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "api",  # I see other using api.apps.ApiConfig here
    "corsheaders",
    "rest_framework",
    'drf_spectacular',
    'rest_framework.authtoken',
    'user',
    #'django.contrib.gis',
]
#registers middleware components
#these components process requests before reaching or leaving a view
#the order is very important in this list for more see https://docs.djangoproject.com/en/5.1/ref/middleware/#middleware-ordering
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#defines where the url patterns are defined
#'core.urls' means urls.py in the core app
ROOT_URLCONF = 'core.urls'

#template stuff. maybe not even requiered since we don't use templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
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

#specifies location of wsgi application
WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# loads env variables for database connection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('VAT_POSTGRES_DB'),
        'USER': os.getenv('VAT_POSTGRES_USER'),
        'PASSWORD': os.getenv('VAT_POSTGRES_PASS'),
        'HOST': os.getenv('VAT_POSTGRES_HOST'),
        'PORT': os.getenv('VAT_POSTGRES_PORT'),
        }   
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

#defines validators for new user passwords
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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://github.com/adamchainz/django-cors-headers
CORS_ALLOW_ALL_ORIGINS = False #we shouldn't to this because it makes the cors allowed origins obsolete
CORS_ALLOWS_CREDENTIALS = False
CORS_ALLOWED_ORIGINS = ['https://api.berlin-united.com','https://vat.berlin-united.com', 'http://localhost:5173', 'http://localhost:8000']

#makes csrf cookie valid on all subdomains
#CSRF_COOKIE_DOMAIN = ".berlin-united.com"
#specifies all domains where django accepts POST requests from with CSRF tokens
CSRF_TRUSTED_ORIGINS = ['https://api.berlin-united.com', 'https://vat.berlin-united.com', 'http://localhost:8000', 'http://localhost:5173']

#requiered if there is a loadbalancer in front of django that forwards requests over http
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#we only want tokenauth in the swagger view
SPECTACULAR_SETTINGS = {
    'AUTHENTICATION_WHITELIST': ['rest_framework.authentication.TokenAuthentication'],
}

#registers our custom user model
AUTH_USER_MODEL = 'user.VATUser' 

#maximum fields allowed in one post request
DATA_UPLOAD_MAX_NUMBER_FIELDS = 30240

CORS_ALLOW_METHODS = [
    'OPTIONS',
    'POST',
    'PUT',
]

# If you need to allow specific headers
CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
]