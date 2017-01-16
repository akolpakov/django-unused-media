# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand
import six.moves

from django_unused_media.cleanup import get_unused_media, remove_empty_dirs

import os


class Command(BaseCommand):

    help = "Clean unused media files which have no reference in models"

    def add_arguments(self, parser):

        parser.add_argument('--noinput', '--no-input',
                            dest='interactive',
                            action='store_false',
                            default=True,
                            help='Do not ask confirmation')

        parser.add_argument('-e', '--exclude',
                            dest='exclude',
                            action='append',
                            default=[],
                            help='Exclude files by mask (only * is supported), can use multiple --exclude')

    def handle(self, *args, **options):

        unused_media = get_unused_media(options.get('exclude') or [])

        if not unused_media:
            self.stdout.write('Nothing to delete. Exit')
            return

        if options.get('interactive'):

            self.stdout.write('These files will be deleted:')

            for f in unused_media:
                self.stdout.write(f)

            # ask user

            if six.moves.input('Are you sure you want to remove %s unused files? (Y/n)' % len(unused_media)) != 'Y':
                self.stdout.write('Interrupted by user. Exit.')
                return

        for f in unused_media:
            self.stdout.write('Remove %s' % f)
            os.remove(os.path.join(settings.MEDIA_ROOT, f))

        remove_empty_dirs()

        self.stdout.write('Done. %s unused files have been removed' % len(unused_media))
