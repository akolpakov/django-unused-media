# -*- coding: utf-8 -*-

import mock
import six

from preggy import expect
from django.core.management import call_command

from .base import BaseTestCase


class TestManagementCommand(BaseTestCase):
    def test_command_call(self):
        expect(call_command('cleanup_unused_media', interactive=False, minimum_file_age=0)).Not.to_be_an_error()

    def test_command_nothing_to_delete(self):
        stdout = six.StringIO()
        call_command('cleanup_unused_media', interactive=False, stdout=stdout, minimum_file_age=0)
        expect(stdout.getvalue().split('\n'))\
            .to_include(u'Nothing to delete. Exit')

    def test_command_not_interactive(self):
        self._media_create('file.txt')

        stdout = six.StringIO()
        call_command('cleanup_unused_media', interactive=False, stdout=stdout, minimum_file_age=0)
        expect(stdout.getvalue().split('\n'))\
            .to_include(u'Done. Total files removed: 1')

        expect(self._media_exists('file.txt')).to_be_false()

    @mock.patch('six.moves.input', return_value='n')
    def test_command_interactive_n(self, mock_input):
        self._media_create(u'file.txt')

        stdout = six.StringIO()
        call_command('cleanup_unused_media', interactive=True, stdout=stdout, minimum_file_age=0)
        expect(stdout.getvalue().split('\n'))\
            .to_include(u'Interrupted by user. Exit.')

        expect(self._media_exists(u'file.txt')).to_be_true()

    @mock.patch('six.moves.input', return_value='Y')
    def test_command_interactive_y(self, mock_input):
        self._media_create(u'file.txt')

        stdout = six.StringIO()
        call_command('cleanup_unused_media', interactive=True, stdout=stdout, minimum_file_age=0)
        expect(stdout.getvalue().split('\n')) \
            .to_include(u'Done. Total files removed: 1')

        expect(self._media_exists(u'file.txt')).to_be_false()

    @mock.patch('six.moves.input', return_value='Y')
    def test_command_interactive_y_with_ascii(self, mock_input):
        self._media_create(u'Тест.txt')

        expected_string = u'Remove {}'.format(self._media_abs_path(u'Тест.txt'))
        if six.PY2:
            expected_string = expected_string.encode('utf-8')

        stdout = six.StringIO()
        call_command('cleanup_unused_media', interactive=True, stdout=stdout, verbosity=2, minimum_file_age=0)
        expect(stdout.getvalue().split('\n')) \
            .to_include(expected_string) \
            .to_include(u'Done. Total files removed: 1')

        expect(self._media_exists(u'Тест.txt')).to_be_false()

    @mock.patch('django_unused_media.management.commands.cleanup_unused_media.remove_empty_dirs')
    def test_command_do_not_remove_dirs(self, mock_remove_empty_dirs):
        self._media_create(u'sub1/sub2/sub3/notused.txt')

        call_command('cleanup_unused_media', interactive=False, minimum_file_age=0)

        mock_remove_empty_dirs.assert_not_called()

    @mock.patch('django_unused_media.management.commands.cleanup_unused_media.remove_empty_dirs')
    def test_command_remove_dirs(self, mock_remove_empty_dirs):
        self._media_create(u'sub1/sub2/sub3/notused.txt')

        call_command('cleanup_unused_media', interactive=False, remove_empty_dirs=True, minimum_file_age=0)

        mock_remove_empty_dirs.assert_called_once()

    def test_command_dry_run(self):
        self._media_create('file.txt')

        stdout = six.StringIO()
        call_command('cleanup_unused_media', interactive=False, dry_run=True, stdout=stdout, minimum_file_age=0)
        expect(stdout.getvalue().split('\n')) \
            .to_include(u'Total files will be removed: 1') \
            .to_include(u'Dry run. Exit.')

        expect(self._media_exists('file.txt')).to_be_true()

    @mock.patch('six.moves.input', return_value='Y')
    def test_command_interactive_silent(self, mock_input):
        self._media_create(u'file.txt')

        stdout = six.StringIO()
        call_command('cleanup_unused_media', interactive=True, stdout=stdout, verbosity=0, minimum_file_age=0)
        expect(stdout.getvalue().split('\n')) \
            .Not.to_include(u'Files to remove:') \
            .Not.to_include(self._media_abs_path(u'file.txt')) \
            .Not.to_include(u'Remove {}'.format(self._media_abs_path(u'file.txt')))

        expect(self._media_exists(u'file.txt')).to_be_false()

    @mock.patch('six.moves.input', return_value='Y')
    def test_command_noninteractive_silent(self, mock_input):
        self._media_create(u'file.txt')

        stdout = six.StringIO()
        call_command('cleanup_unused_media', interactive=False, stdout=stdout, verbosity=0, minimum_file_age=0)
        expect(stdout.getvalue()).to_equal('')
        expect(self._media_exists(u'file.txt')).to_be_false()
