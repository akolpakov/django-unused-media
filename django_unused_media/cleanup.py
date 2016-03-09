from django.db import models
from django.conf import settings

import os


def _get_file_fields():
    """
        Get all fields which are inherited from FileField
    """

    fields = []

    for m in models.get_models():
        for f in m._meta.get_fields():
            if isinstance(f, models.FileField):
                fields.append(f)

    return fields

def get_used_media():
    """
        Get media which are still used in models
    """

    media = []

    for f in _get_file_fields():
        is_null = {
            '%s__isnull' % f.name: True,
        }
        is_empty = {
            '%s' % f.name: '',
        }

        for t in f.model.objects.values(f.name).exclude(**is_empty).exclude(**is_null):
            media.append(os.path.join(settings.MEDIA_ROOT, t.get(f.name)))

    return media

def _get_all_media():
    """
        Get media which are not used in models
    """

    media = []

    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for name in files:
            media.append(os.path.join(root, name))

    return media

def get_unused_media():
    all_media = _get_all_media()
    used_media = get_used_media()

    return [t for t in all_media if t not in used_media]
