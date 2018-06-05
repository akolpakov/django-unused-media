# -*- coding: utf-8 -*-

import os
import re

import six
from django.conf import settings
from django.core.validators import EMPTY_VALUES

from .remove import remove_media
from .utils import append_if_not_exists, get_file_fields


def get_used_media():
    """
        Get media which are still used in models
    """

    media = []

    for field in get_file_fields():
        is_null = {
            '%s__isnull' % field.name: True,
        }
        is_empty = {
            '%s' % field.name: '',
        }

        storage = field.storage

        for value in field.model.objects \
                .values_list(field.name, flat=True) \
                .exclude(**is_empty).exclude(**is_null):
            if value not in EMPTY_VALUES:
                append_if_not_exists(media, storage.path(value))

    return media


def get_all_media(exclude=None):
    """
        Get all media from MEDIA_ROOT
    """

    if not exclude:
        exclude = []

    media = []

    for root, dirs, files in os.walk(six.text_type(settings.MEDIA_ROOT)):
        for name in files:
            path = os.path.abspath(os.path.join(root, name))
            relpath = os.path.relpath(path, settings.MEDIA_ROOT)
            in_exclude = False
            for e in exclude:
                if re.match(r'^%s$' % re.escape(e).replace('\\*', '.*'), relpath):
                    in_exclude = True
                    break

            if not in_exclude:
                append_if_not_exists(media, path)

    return media


def get_unused_media(exclude=None):
    """
        Get media which are not used in models
    """

    if not exclude:
        exclude = []

    all_media = get_all_media(exclude)
    used_media = get_used_media()

    return [x for x in all_media if x not in used_media]


def remove_unused_media():
    """
        Remove unused media
    """
    remove_media(get_unused_media())
