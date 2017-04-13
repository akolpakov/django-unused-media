# -*- coding: utf-8 -*-

import os
import re

import six
from django.apps import apps
from django.conf import settings
from django.db import models


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

    for m in all_models:
        for f in m._meta.get_fields():
            if isinstance(f, models.FileField):
                fields.append(f)

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

        if hasattr(field, 'variations'):  # django-stdimage has a variatons field for different sizes of images
            image_varitions = [key for key, val in field.variations.iteritems()]  # get key names for variations

            for model_obj in field.model.objects.exclude(**is_empty).exclude(**is_null):
                image_field = getattr(model_obj, field.name)

                media.append(six.text_type(image_field))  # Original image is used

                for variant in image_varitions:  # Check if variant of image exists
                    variant_image = getattr(image_field, variant, None)
                    if variant_image:
                        media.append(six.text_type(variant_image))
        else:
            for t in field.model.objects.values(field.name).exclude(**is_empty).exclude(**is_null):
                media.append(six.text_type(t.get(field.name)))

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
            rel_path = os.path.relpath(os.path.join(root, name), settings.MEDIA_ROOT)
            in_exclude = False
            for e in exclude:
                if re.match(r'^%s$' % re.escape(e).replace('\\*', '.*'), rel_path):
                    in_exclude = True
                    break

            if not in_exclude:
                media.append(rel_path)

    return media


def get_unused_media(exclude=None):
    """
        Get media which are not used in models
    """

    if not exclude:
        exclude = []

    all_media = _get_all_media(exclude)
    used_media = get_used_media()

    for i in xrange(len(used_media)):  # Sometimes the image returned has a ./img.jpg format, which doesnt match.
        if used_media[i][0:2] == './':
            used_media[i] = used_media[i].replace('./', '')

    return [t for t in all_media if t not in used_media]


def _remove_media(files):
    """
        Delete file from media dir
    """
    for f in files:
        os.remove(os.path.join(settings.MEDIA_ROOT, f))


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
