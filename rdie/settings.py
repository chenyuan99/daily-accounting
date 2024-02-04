from pathlib import Path
import os
import json
import django_heroku
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "9=kq$9byi(&1#^*m@xm_t6=2+@@ny@g+a%cg_fl*^a#--m)&4w"
DEBUG = True
ALLOWED_HOSTS = ['*']
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_filters",
    'crispy_forms',
    'rest_framework',
    'accounting',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rdie.urls'

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

WSGI_APPLICATION = 'rdie.wsgi.application'

DATABASES = {
    "default": dj_database_url.parse(
        "postgres://fafnvlvssyhxdd:9eb477360418f8141e95b90ffeb3bd4868adedcd7ec750e64355d23759dd8a56@ec2-52-23-131-232"
        ".compute-1.amazonaws.com:5432/d7n6hekl6rpir6")
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# config/settings.py
LOGIN_REDIRECT_URL = '/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
django_heroku.settings(locals())
IMPORT_EXPORT_USE_TRANSACTIONS = True
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# adding config
cloudinary.config(
    cloud_name="hl7a3okqn",
    api_key="611729113638181",
    api_secret="VdRJwqMXOhhUltwYAyG6AKwTmsU"
)
