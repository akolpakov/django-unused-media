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
        
        parser.add_argument('--remove-empty-dirs',
                            dest='remove_empty_dirs',
                            action='store_false',
                            default=False,
                            help='Remove empty dirs after files cleanup')

        parser.add_argument('-n', '--dry-run',
                            dest='dry_run',
                            action='store_true',
                            default=False,
                            help='Do everything except modify the filesystem.')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        unused_media = get_unused_media(options.get('exclude') or [])

        if not unused_media:
            self.stdout.write('Nothing to delete. Exit')
            return

        if options.get('interactive'):

            self.stdout.write('These files will be deleted:')

            for f in unused_media:
                self.stdout.write(f)

            # ask user

            if six.moves.input('Are you sure you want to remove %s unused files? (y/N)' % len(unused_media)).upper() != 'Y':
                self.stdout.write('Interrupted by user. Exit.')
                return

        for f in unused_media:
            if dry_run:
                self.stdout.write('Pretending to remove %s' % f)
            else:
                self.stdout.write('Remove %s' % f)
                os.remove(os.path.join(settings.MEDIA_ROOT, f))

        if not dry_run and options.get('remove_empty_dirs'):
            remove_empty_dirs()

        self.stdout.write('Done. %s unused files have been removed' % len(unused_media))
