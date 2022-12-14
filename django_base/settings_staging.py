from settings import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'guwen_staging',
        'USER': 'meta_db_user',
        'PASSWORD': 'Rutz05#HH',
        'HOST': '',
        'PORT': '',
        }
    }

STATIC_ROOT = '/home/rmoor/webapps/guwen_staging_nginx/static/'
MEDIA_ROOT = '/home/rmoor/webapps/guwen_staging_nginx/media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'guwen'
EMAIL_HOST_PASSWORD = '5d8ka2&a'
DEFAULT_FROM_EMAIL = 'webmaser@guwen.rubenmoor.net'
SERVER_EMAIL = 'webmaser@guwen.rubenmoor.net'

# not working
ADMINS = (('Ruben', 'ruben.moor@gmail.com'),)

ALLOWED_HOSTS = ['.rubenmoor.net', '.mdrexl.de']
