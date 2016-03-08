from django.db import models


def get_file_fields():
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
        Get media which are still using in models
    """

    media = []

    for f in get_file_fields():
        is_null = {
            '%s__isnull' % f.name: True,
        }
        is_empty = {
            '%s' % f.name: '',
        }

        for t in f.model.objects.values(f.name).exclude(**is_empty).exclude(**is_null):
            media.append(t.get(f.name))

    return media
