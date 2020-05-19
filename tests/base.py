# -*- coding: utf-8 -*-

import shutil
import os
import time

from django.test import TestCase
from django.conf import settings
from django.core.files.base import ContentFile


class BaseTestCase(TestCase):
    def setUp(self):
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)

        os.makedirs(settings.MEDIA_ROOT)

    def tearDown(self):
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)

    @classmethod
    def _create_file(cls, filename, data=None):
        if not data:
            data = 'test'
        return ContentFile(data, filename)

    @classmethod
    def _create_image(cls, filename):
        with open(os.path.join(settings.TEST_DIR, 'sample.jpg'), 'rb') as f:
            image = cls._create_file(filename, f.read())
        return image

    @classmethod
    def _media_abs_path(cls, filename):
        return os.path.join(settings.MEDIA_ROOT, filename)

    @classmethod
    def _media_exists(cls, filename):
        return os.path.exists(cls._media_abs_path(filename))

    @classmethod
    def _media_create(cls, filename, data=None, file_age=None):
        if not data:
            data = 'test'

        filename = cls._media_abs_path(filename)

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, 'w') as f:
            f.write(data)

        if file_age:
            modification_time = time.time() - file_age
            os.utime(filename, (modification_time, modification_time))
