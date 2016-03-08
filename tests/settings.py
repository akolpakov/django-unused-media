import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

INSTALLED_APPS = (
    'django_unused_media',
)

SECRET_KEY = 'test'

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = os.path.join(TEST_DIR, 'media')
