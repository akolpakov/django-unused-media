# -*- coding: utf-8 -*-

import mock
import six

from preggy import expect
from django.core.management import call_command

from django_unused_media.management.commands.cleanup_unused_media import Command
from .base import BaseTestCase


class TestManagementCommand(BaseTestCase):
    def test_command_call(self):
        expect(call_command('cleanup_unused_media', interactive=False)).Not.to_be_an_error()

    def test_command_nothing_to_delete(self):
        cmd = Command()
        cmd.handle(interactive=False)
        expect(cmd.stdout.getvalue().split('\n'))\
            .to_include(u'Nothing to delete. Exit')

    def test_command_not_interactive(self):
        self._media_create('file.txt')

        cmd = Command()
        cmd.handle(interactive=False)
        expect(cmd.stdout.getvalue().split('\n'))\
            .to_include(u'Remove {}'.format(self._media_abs_path(u'file.txt')))\
            .to_include(u'Done. 1 unused files have been removed')

        expect(self._media_exists('file.txt')).to_be_false()

    @mock.patch('six.moves.input', return_value='n')
    def test_command_interactive_n(self, mock_input):
        self._media_create(u'file.txt')

        cmd = Command()
        cmd.handle(interactive=True)
        expect(cmd.stdout.getvalue().split('\n'))\
            .to_include(u'Interrupted by user. Exit.')

        expect(self._media_exists(u'file.txt')).to_be_true()

    @mock.patch('six.moves.input', return_value='Y')
    def test_command_interactive_y(self, mock_input):
        self._media_create(u'file.txt')

        cmd = Command()
        cmd.handle(interactive=True)
        expect(cmd.stdout.getvalue().split('\n')) \
            .to_include(u'Remove {}'.format(self._media_abs_path(u'file.txt'))) \
            .to_include(u'Done. 1 unused files have been removed')

        expect(self._media_exists(u'file.txt')).to_be_false()

    @mock.patch('six.moves.input', return_value='Y')
    def test_command_interactive_y_with_ascii(self, mock_input):
        self._media_create(u'Тест.txt')

        expected_string = u'Remove {}'.format(self._media_abs_path(u'Тест.txt'))
        if six.PY2:
            expected_string = expected_string.encode('utf-8')

        cmd = Command()
        cmd.handle(interactive=True)
        expect(cmd.stdout.getvalue().split('\n')) \
            .to_include(expected_string) \
            .to_include(u'Done. 1 unused files have been removed')

        expect(self._media_exists(u'Тест.txt')).to_be_false()
