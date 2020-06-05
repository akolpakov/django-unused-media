# -*- coding: utf-8 -*-

import os
import re
import time

import six
from django.conf import settings
from django.core.validators import EMPTY_VALUES

from .remove import remove_media
from .utils import get_file_fields


def get_used_media():
    """
        Get media which are still used in models
    """

    media = set()

    for field in get_file_fields():
        is_null = {
            '%s__isnull' % field.name: True,
        }
        is_empty = {
            '%s' % field.name: '',
        }

        storage = field.storage

        for value in field.model._base_manager \
                .values_list(field.name, flat=True) \
                .exclude(**is_empty).exclude(**is_null):
            if value not in EMPTY_VALUES:
                media.add(storage.path(value))

    return media


def get_all_media(exclude=None, minimum_file_age=None):
    """
        Get all media from MEDIA_ROOT
    """

    if not exclude:
        exclude = []

    media = set()
    initial_time = time.time()

    for root, dirs, files in os.walk(six.text_type(settings.MEDIA_ROOT)):
        for name in files:
            path = os.path.abspath(os.path.join(root, name))
            relpath = os.path.relpath(path, settings.MEDIA_ROOT)

            if minimum_file_age:
                file_age = initial_time - os.path.getmtime(path)
                if file_age < minimum_file_age:
                    continue

            for e in exclude:
                if re.match(r'^%s$' % re.escape(e).replace('\\*', '.*'), relpath):
                    break
            else:
                media.add(path)

    return media


def get_unused_media(exclude=None, minimum_file_age=None):
    """
        Get media which are not used in models
    """

    if not exclude:
        exclude = []

    all_media = get_all_media(exclude, minimum_file_age)
    used_media = get_used_media()

    return all_media - used_media


def remove_unused_media():
    """
        Remove unused media
    """
    remove_media(get_unused_media())
