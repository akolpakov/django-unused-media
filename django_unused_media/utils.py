# -*- coding: utf-8 -*-

import os
import platform
import time

from django.apps import apps
from django.db import models


def get_file_fields():
    """
        Get all fields which are inherited from FileField
    """

    # get models

    all_models = apps.get_models()

    # get fields

    fields = []

    for model in all_models:
        for field in model._meta.get_fields():
            if isinstance(field, models.FileField):
                fields.append(field)

    return fields


def file_age_sec(path_to_file):
    if platform.system() == 'Windows':
        mtime = os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        mtime = stat.st_mtime

    return time.time() - mtime
