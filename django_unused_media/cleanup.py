# -*- coding: utf-8 -*-

from django.db import models
from django.apps import apps
from django.conf import settings

import os
import re
import six


def _get_file_fields():
    """
        Get all fields which are inherited from FileField
    """

    # get models. Compatibility with 1.6

    if getattr(apps, 'get_models'):
        all_models = apps.get_models()
    else:
        all_models = models.get_models()

    # get fields

    fields = []

    for model in all_models:
        for field in model._meta.get_fields():
            if isinstance(field, models.FileField):
                fields.append(field)

    return fields


def get_used_media():
    """
        Get media which are still used in models
    """

    media = []

    for field in _get_file_fields():
        is_null = {
            '%s__isnull' % field.name: True,
        }
        is_empty = {
            '%s' % field.name: '',
        }

        for obj in field.model.objects.exclude(**is_empty).exclude(**is_null):
            media.append(getattr(obj, field.name).path)

    return media


def _get_all_media(exclude=None):
    """
        Get all media from MEDIA_ROOT
    """

    if not exclude:
        exclude = []

    media = []

    for root, dirs, files in os.walk(six.text_type(settings.MEDIA_ROOT)):
        for name in files:
            path = os.path.join(root, name)
            relpath = os.path.relpath(path, settings.MEDIA_ROOT)
            in_exclude = False
            for e in exclude:
                if re.match(r'^%s$' % re.escape(e).replace('\\*', '.*'), relpath):
                    in_exclude = True
                    break

            if not in_exclude:
                media.append(path)

    return media


def get_unused_media(exclude=None):
    """
        Get media which are not used in models
    """

    if not exclude:
        exclude = []

    all_media = _get_all_media(exclude)
    used_media = get_used_media()

    return [x for x in all_media if x not in used_media]


def _remove_media(files):
    """
        Delete file from media dir
    """
    for file in files:
        os.remove(os.path.join(settings.MEDIA_ROOT, file))


def remove_unused_media():
    """
        Remove unused media
    """
    _remove_media(get_unused_media())


def remove_empty_dirs(path=settings.MEDIA_ROOT):
    """
        Recursively delete empty directories; return True if everything was deleted.
    """

    if not os.path.isdir(path):
        return False

    if all([remove_empty_dirs(os.path.join(path, filename)) for filename in os.listdir(path)]):
        os.rmdir(path)
        return True
    else:
        return False
