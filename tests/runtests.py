# -*- coding: utf-8 -*-

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django_nose import NoseTestSuiteRunner


if __name__ == '__main__':
    NoseTestSuiteRunner(verbosity=1).run_tests(['tests'])
