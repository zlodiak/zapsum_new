# -*- coding: utf-8 -*-

"""
Django settings for zapsum project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

#SITE_ID = 1


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xbn7_ppbheu@d%8igbwiu5kxxe4p!pk)v#=u)4^3buw-cbb_nz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.flatpages',
    #'django.contrib.sites',

    'sorl.thumbnail',
    'django_summernote', 
    'captcha', 

    'app_zapsum',
    'app_accounts',
    'app_messages',
    'app_guestbook',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',   
)

ROOT_URLCONF = 'zapsum.urls'

WSGI_APPLICATION = 'zapsum.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'zapsum', # имя БД                       
#         'USER': 'zapsum', # пользователь СУБД
#         'PASSWORD': 'rootybroot', # пароль пользователя
#         'HOST': '127.0.0.1',  # адрес               
#         'PORT': '3306', # установить порт СУБД, по умолчанию 3306 для mysql             
#     }
# }


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    (os.path.join(BASE_DIR, "zapsum/static/")),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'zapsum/templates/'),
    os.path.join(BASE_DIR, 'app_zapsum/templates/'),
    os.path.join(BASE_DIR, 'app_accounts/templates/'),
    os.path.join(BASE_DIR, 'app_messages/templates/'),
    os.path.join(BASE_DIR, 'app_guestbook/templates/'),
)



THUMBNAIL_DEBUG = False


ALLOWED_HOSTS = ['127.0.0.1:8000']
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


SOUTH_MIGRATION_MODULES = {
    'captcha': 'captcha.south_migrations',
}


