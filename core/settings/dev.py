from .base import * 

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

MEDIA_URL = "/media/"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}