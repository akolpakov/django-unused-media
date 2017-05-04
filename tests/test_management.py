# -*- coding: utf-8 -*-

import mock
import sys
import six

from preggy import expect
from django.db import models
from django.core.management import call_command

from django_unused_media.cleanup import _get_file_fields, _get_all_media, get_used_media, get_unused_media, _remove_media, remove_unused_media, remove_empty_dirs
from django_unused_media.management.commands.cleanup_unused_media import Command
from .base import BaseTestCase
from .models import FileFieldsModel, CustomFileldsModel
from .utils import create_file, create_image, create_file_and_write, exists_media_path


_ver = sys.version_info


class TestManagementCommand(BaseTestCase):
    def test_command_call(self):
        expect(call_command('cleanup_unused_media', interactive=False)).Not.to_be_an_error()

    def test_command_nothing_to_delete(self):
        cmd = Command()
        cmd.handle(interactive=False)
        expect(cmd.stdout.getvalue().split('\n'))\
            .to_include('Nothing to delete. Exit')

    def test_command_not_interactive(self):
        create_file_and_write('file.txt')

        cmd = Command()
        cmd.handle(interactive=False)
        expect(cmd.stdout.getvalue().split('\n'))\
            .to_include('Remove file.txt')\
            .to_include('Done. 1 unused files have been removed')

        expect(exists_media_path('file.txt')).to_be_false()

    @mock.patch('six.moves.input', return_value='n')
    def test_command_interactive_n(self, mock_input):
        create_file_and_write(u'file.txt')

        cmd = Command()
        cmd.handle(interactive=True)
        expect(cmd.stdout.getvalue().split('\n'))\
            .to_include('Interrupted by user. Exit.')

        expect(exists_media_path(u'file.txt')).to_be_true()

    @mock.patch('six.moves.input', return_value='Y')
    def test_command_interactive_y(self, mock_input):
        create_file_and_write(u'file.txt')

        cmd = Command()
        cmd.handle(interactive=True)
        expect(cmd.stdout.getvalue().split('\n'))\
            .to_include('Remove file.txt')\
            .to_include('Done. 1 unused files have been removed')

        expect(exists_media_path(u'file.txt')).to_be_false()

    @mock.patch('six.moves.input', return_value='Y')
    def test_command_interactive_y_with_ascii(self, mock_input):
        create_file_and_write(u'Тест.txt')

        cmd = Command()
        cmd.handle(interactive=True)
        expect(cmd.stdout.getvalue().split('\n'))\
            .to_include('Remove Тест.txt')\
            .to_include('Done. 1 unused files have been removed')

        expect(exists_media_path(u'Тест.txt')).to_be_false()
