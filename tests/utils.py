# -*- coding: utf-8 -*-

from django.core.files.base import ContentFile
from django.conf import settings

import os


def create_file(filename, data=None):
    if not data:
        data = 'test'
    return ContentFile(data, filename)


def create_image(filename):
    with open(os.path.join(settings.TEST_DIR, 'sample.jpg'), 'rb') as f:
        image = create_file(filename, f.read())
    return image

def get_media_path(filename):
    return os.path.join(settings.MEDIA_ROOT, filename)

def exists_media_path(filename):
    return os.path.exists(get_media_path(filename))

def create_file_and_write(filename, data=None):
    if not data:
        data = 'test'

    filename = get_media_path(filename)

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    with open(filename, 'w') as f:
        f.write(data)
