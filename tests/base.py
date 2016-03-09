# -*- coding: utf-8 -*-

import shutil
import os
from django.test import TestCase
from django.conf import settings


class BaseTestCase(TestCase):
    def setUp(self):
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)

        os.makedirs(settings.MEDIA_ROOT)

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)
