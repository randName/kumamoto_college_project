import dj_database_url

from .base import *

DEBUG = False

INSTALLED_APPS += ('mod_wsgi.server',)

DATABASES['default'] = dj_database_url.config(conn_max_age=500)

STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT')
