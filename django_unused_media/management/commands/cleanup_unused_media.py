# -*- coding: utf-8 -*-

import os

import six.moves
from django.conf import settings
from django.core.management.base import BaseCommand

from django_unused_media.cleanup import get_unused_media
from django_unused_media.remove import remove_empty_dirs


class Command(BaseCommand):

    help = "Clean unused media files which have no reference in models"

    # verbosity
    # 0 means silent
    # 1 means normal output (default).
    # 2 means verbose output

    verbosity = 1

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

        parser.add_argument('--minimum-file-age',
                            dest='minimum_file_age',
                            default=60,
                            type=int,
                            nargs=1,
                            help='Skip files younger this age (sec)')

        parser.add_argument('--remove-empty-dirs',
                            dest='remove_empty_dirs',
                            action='store_false',
                            default=False,
                            help='Remove empty dirs after files cleanup')

        parser.add_argument('-n', '--dry-run',
                            dest='dry_run',
                            action='store_true',
                            default=False,
                            help='Dry run without any affect on your data')

    def info(self, message):
        if self.verbosity > 0:
            self.stdout.write(message)

    def debug(self, message):
        if self.verbosity > 1:
            self.stdout.write(message)

    def _show_files_to_delete(self, unused_media):
        self.debug('Files to remove:')

        for f in unused_media:
            self.debug(f)

        self.info('Total files will be removed: {}'.format(len(unused_media)))

    def handle(self, *args, **options):

        if 'verbosity' in options:
            self.verbosity = options['verbosity']

        unused_media = get_unused_media(
            exclude=options.get('exclude'),
            minimum_file_age=options.get('minimum_file_age'),
        )

        if not unused_media:
            self.info('Nothing to delete. Exit')
            return

        if options.get('dry_run'):
            self._show_files_to_delete(unused_media)
            self.info('Dry run. Exit.')
            return

        if options.get('interactive'):
            self._show_files_to_delete(unused_media)

            # ask user

            question = 'Are you sure you want to remove {} unused files? (y/N)'.format(len(unused_media))

            if six.moves.input(question).upper() != 'Y':
                self.info('Interrupted by user. Exit.')
                return

        for f in unused_media:
            self.debug('Remove %s' % f)
            os.remove(os.path.join(settings.MEDIA_ROOT, f))

        if options.get('remove_empty_dirs'):
            remove_empty_dirs()

        self.info('Done. Total files removed: {}'.format(len(unused_media)))
