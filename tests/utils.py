try:
    from cStringIO import cStringIO as BytesIO
except ImportError:
    from django.utils.six import BytesIO

try:
    from PIL import Image
except ImportError:
    import Image

from django.core.files.base import ContentFile


def create_file(filename, data=None):
    if not data:
        data = 'test'
    return ContentFile(data, filename)


def create_image(filename, size=(800, 600), image_mode='RGB', image_format='JPEG'):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    return create_file(filename, data.read())
