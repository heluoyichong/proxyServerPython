# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging
import django.utils.log
import logging.handlers

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6py^p$o)al2qtq1qaz!kj!txs*&ri&rqp#e7el#z41*mlcpcvm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#LOGGING_CONFIG = None

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "template"),
)

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
#    'django.contrib.admin',
#    'django.contrib.auth',
#    'django.contrib.contenttypes',
    'django.contrib.sessions',
#    'django.contrib.messages',
    'django.contrib.staticfiles',
    'proxyserver.app.main',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
#    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'proxyserver.urls'

WSGI_APPLICATION = 'proxyserver.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': '1234qwer',
        'HOST': 'localhost',   
        'PORT': '3306',
    },
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Logging config
LOG_DIR = os.path.join(BASE_DIR, "log/server.log")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
       'standard': {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR,
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR,
            'maxBytes':1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR,
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'scprits_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':LOG_DIR,
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'scripts': {
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'app.debug': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}
