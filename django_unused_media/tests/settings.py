import os

SECRET_KEY = 'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = (
    'django_unused_media',
    'django_unused_media.tests',
)

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = os.path.join(TEST_DIR, 'media')