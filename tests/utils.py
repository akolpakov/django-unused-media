from django.core.files.base import ContentFile
from django.conf import settings


def create_file(filename, data=None):
    if not data:
        data = 'test'
    return ContentFile(data, filename)


def create_image(filename):
    with open('%s/sample.jpg' % settings.TEST_DIR, 'r') as f:
        image = create_file(filename, f.read())
    return image
