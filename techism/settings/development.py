
### import base settings

from base import *


### development specific settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'techism.sqlite', 
    }
}

WSGI_APPLICATION = 'techism.settings.development_wsgi.application'

SESSION_COOKIE_SECURE = False
HTTPS_PATHS = (
#    '/admin/',
#    '/accounts/',
)
HTTP_URL = 'http://localhost:8000'
HTTPS_URL = 'https://localhost:8443'

try:
    from debug_toolbar.middleware import DebugToolbarMiddleware
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INTERNAL_IPS = ('127.0.0.1',)
    INSTALLED_APPS += ('debug_toolbar',)
except ImportError:
    pass

### import settings stored in database

from database import *
