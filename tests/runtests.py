# -*- coding: utf-8 -*-

import os

from django_nose import NoseTestSuiteRunner


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


if __name__ == '__main__':
    if NoseTestSuiteRunner(verbosity=1).run_tests(['tests']) > 0:
        exit(1)
    else:
        exit(0)
