# -*- coding: utf-8 -*-

from django.db import models


# Custom field

class CustomFiled(models.FileField):
    pass


# Test models

class FileFieldsModel(models.Model):
    file_field = models.FileField(upload_to='test1')
    image_field = models.ImageField(upload_to='test1_image')
    char_field = models.CharField(max_length=255)


class CustomFileldsModel(models.Model):
    custom_field = CustomFiled(upload_to='sub/dir/test2', null=True, blank=True)
    char_field = models.CharField(max_length=255)


class CustomManager(models.Manager):
    def get_queryset(self):
        return super(CustomManager, self).get_queryset().filter(active=True)


class CustomManagerModel(models.Model):
    active = models.BooleanField(default=True)
    file_field = models.FileField(upload_to='test3')

    objects = CustomManager()
