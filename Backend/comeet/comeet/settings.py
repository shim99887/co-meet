"""
Django settings for comeet project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h@us1+p%s(rv@+cs^%rpx(r686)sdy47%atshhd76$&0_$(ur3'

# SECURITY WARNING: don't run with debug turned on in production!
# 개발 시 로그를 무조건 남긴다.
# 운영시에는 False로 변경을 해준다.
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'j4a203.p.ssafy.io', '127.0.0.1']

# Swagger Setting
SWAGGER_SETTINGS = {
    'USER_SESSION_AUTH': False
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user.apps.UserConfig',
    'api.apps.ApiConfig',
    'recomm.apps.RecommConfig',
    'corsheaders',
    'drf_yasg',  # Swagger
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    'http://localhost:8080',
)

ROOT_URLCONF = 'comeet.urls'

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

WSGI_APPLICATION = 'comeet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': str(os.path.join(BASE_DIR, "db.sqlite3"))
    # },
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'comeet',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
                'host': 'j4a203.p.ssafy.io',
                'port': 8888,
                'username': 'comeet',
                'password': 'yb)&.2Ewyy+C?5&~T=,{<D,S!w',
                'authSource': 'admin',
                'authMechanism': 'SCRAM-SHA-1'
        },
        'LOGGING': {
            'version': 1,
            'loggers': {
                'djongo': {
                    'level': 'DEBUG',
                    'propagate': False,
                }
            },
        },
    }
}

# Cache

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://127.0.0.1:6379/1",
        "LOCATION": "redis://j4a203.p.ssafy.io:6379/1",
        "OPTIONS": {
            "PASSWORD": "yb)&.2Ewyy+C?5&~T=,{<D,S!w",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Google Email
SITE_ID = 1

DEFAULT_FROM_EMAIL = 'comeetmanager@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'comeetmanager@gmail.com'
EMAIL_HOST_PASSWORD = 'comeet1234'
SERVER_EMAIL = 'comeetmanager'
REDIRECT_PAGE = 'https://j4a203.p.ssafy.io'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.fAttributeSimilarityValidator',
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

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
