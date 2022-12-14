from settings import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'guwen',
        'USER': 'guwen',
        'PASSWORD': 'guwen-Rw7_0zdFQiavh4',
        'HOST': 'mysql',
        'PORT': '',
        }
    }

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'meta_mailbox'
EMAIL_HOST_PASSWORD = '5d8ka2&a'
DEFAULT_FROM_EMAIL = 'webmaster@guwen.rubenmoor.net'
SERVER_EMAIL = 'webmaster@guwen.rubenmoor.net'

ADMINS = (('Ruben', 'ruben.moor@gmail.com'),)

ALLOWED_HOSTS = ['.rubenmoor.net', '.mdrexl.de','.b028.blue.fastwebserver.de']
