import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()


class DjangoTests(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from django.core import management
        if 'DJANGO_SETTINGS_MODULE' not in os.environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = 'django_unused_media.tests.settings'
        management.execute_from_command_line()

setup(
    name = 'django-unused-media',
    version = '0.0.1',
    author = 'Andrey Kolpakov',
    author_email = 'aakolpakov@gmail.com',
    description = 'Remove unused media files',

    license = 'MIT License',
    keywords = 'django unused media cleanup obsolete',
    url = 'https://github.com/akolpakov/django-unused-media',
    packages=find_packages(),
    long_description=read('README.rst'),

    cmdclass={'test': DjangoTests},

    install_requires=[
        'Django >= 1.4.3',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries'
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
)