# -*- coding: utf-8 -*-

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
