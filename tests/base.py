import shutil
import os
from django.test import TestCase
from django.conf import settings


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT)
