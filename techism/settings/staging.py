
### import base settings

from base import *


### staging specific settings

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = (
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'techisms', 
    }
}

WSGI_APPLICATION = 'techism.settings.staging_wsgi.application'

SESSION_COOKIE_SECURE = True
HTTPS_PATHS = (
    '/admin/',
    '/accounts/',
)
HTTP_URL = 'http://next.techism.de'
HTTPS_URL = 'https://next.techism.de'


### import settings stored in database

from database import *
