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


class UtilsTestCase(BaseTestCase):
    def setUp(self):
        super(UtilsTestCase, self).setUp()

        self.model1 = FileFieldsModel(
            file_field=create_file('file1.txt'),
            image_field=create_image('image1.jpg'),
            char_field='test1'
        )
        self.model1.save()

        self.model2 = FileFieldsModel(
            file_field=create_file('file2.txt'),
            image_field=create_image('image2.jpg'),
            char_field='test2'
        )
        self.model2.save()

        self.model3 = CustomFileldsModel(
            custom_field=create_file('file3.txt'),
            char_field='test3'
        )
        self.model3.save()

        self.model4 = CustomFileldsModel(
            char_field='test4'
        )
        self.model4.save()

    def test_get_file_fields(self):
        file_fields = _get_file_fields()
        expect(file_fields).to_be_instance_of(list).to_length(3)

        for f in file_fields:
            expect(f).to_be_instance_of(models.FileField)

        file_fields_names = [f.name for f in file_fields]

        expect(file_fields_names).to_include('file_field').to_include('image_field').to_include('custom_field')
        expect(file_fields_names).Not.to_include('char_field')

    def test_get_used_media(self):
        expect(get_used_media())\
            .to_be_instance_of(list).to_length(5)\
            .to_include(self.model1.file_field.name)\
            .to_include(self.model1.image_field.name)\
            .to_include(self.model2.file_field.name)\
            .to_include(self.model2.image_field.name)\
            .to_include(self.model3.custom_field.name)

    def test_get_all_media(self):
        expect(_get_all_media())\
            .to_be_instance_of(list).to_length(5)\
            .to_include(self.model1.file_field.name)\
            .to_include(self.model1.image_field.name)\
            .to_include(self.model2.file_field.name)\
            .to_include(self.model2.image_field.name)\
            .to_include(self.model3.custom_field.name)

    def test_get_all_media_with_additional(self):
        create_file_and_write(u'file.txt')
        expect(_get_all_media())\
            .to_be_instance_of(list).to_length(6)\
            .to_include(self.model1.file_field.name)\
            .to_include(self.model1.image_field.name)\
            .to_include(self.model2.file_field.name)\
            .to_include(self.model2.image_field.name)\
            .to_include(self.model3.custom_field.name)\
            .to_include(u'file.txt')

    def test_get_all_media_with_exclude(self):
        create_file_and_write(u'file.txt')
        create_file_and_write(u'.file2.txt')
        create_file_and_write(u'test.txt')
        create_file_and_write(u'do_not_exclude/test.txt')
        create_file_and_write(u'one.png')
        create_file_and_write(u'two.png')
        create_file_and_write(u'three.png')
        expect(_get_all_media(['.*', '*.png', 'test.txt']))\
            .to_be_instance_of(list).to_length(7)\
            .to_include(self.model1.file_field.name)\
            .to_include(self.model1.image_field.name)\
            .to_include(self.model2.file_field.name)\
            .to_include(self.model2.image_field.name)\
            .to_include(self.model3.custom_field.name)\
            .to_include(u'file.txt')\
            .Not.to_include(u'.file2.txt')\
            .Not.to_include(u'test.txt')\
            .to_include(u'do_not_exclude/test.txt')

    def test_get_all_media_with_exclude_folder(self):
        create_file_and_write(u'exclude_dir/file1.txt')
        create_file_and_write(u'exclude_dir/file2.txt')
        create_file_and_write(u'file3.txt')
        expect(_get_all_media(['exclude_dir/*']))\
            .to_be_instance_of(list).to_length(6)\
            .to_include(self.model1.file_field.name)\
            .to_include(self.model1.image_field.name)\
            .to_include(self.model2.file_field.name)\
            .to_include(self.model2.image_field.name)\
            .to_include(self.model3.custom_field.name)\
            .to_include(u'file3.txt')\
            .Not.to_include(u'exclude_dir/file1.txt')\
            .Not.to_include(u'exclude_dir/file2.txt')

    def test_get_unused_media_empty(self):
        expect(get_unused_media()).to_be_empty()

    def test_get_unused_media(self):
        create_file_and_write(u'notused.txt')
        used_media = get_unused_media()
        expect(used_media).to_be_instance_of(list).to_length(1)
        expect(used_media[0]).to_match(r'^.*notused.txt')

    def test_get_unused_media_subfolder(self):
        create_file_and_write(u'subfolder/notused.txt')
        used_media = get_unused_media()
        expect(used_media).to_be_instance_of(list).to_length(1)
        expect(used_media[0]).to_match(r'^.*subfolder/notused.txt$')

    def test_remove_media(self):
        expect(exists_media_path(u'file.txt')).to_be_false()
        create_file_and_write(u'file.txt')
        expect(exists_media_path(u'file.txt')).to_be_true()
        _remove_media([u'file.txt'])
        expect(exists_media_path(u'file.txt')).to_be_false()

    def test_remove_unused_media(self):
        expect(get_unused_media()).to_be_empty()
        create_file_and_write(u'notused.txt')
        expect(get_unused_media()).Not.to_be_empty()
        remove_unused_media()
        expect(get_unused_media()).to_be_empty()

    def test_remove_empty_dirs(self):
        create_file_and_write(u'sub1/sub2/sub3/notused.txt')
        remove_unused_media()
        remove_empty_dirs()
        expect(exists_media_path(u'sub1/sub2/sub3')).to_be_false()
        expect(exists_media_path(u'sub1/sub2')).to_be_false()
        expect(exists_media_path(u'sub1')).to_be_false()

    # Management command

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

    def test_ascii_filenames(self):
        create_file_and_write(u'Тест.txt')
        used_media = get_unused_media()
        expect(used_media).to_be_instance_of(list).to_length(1)
        expect(used_media[0]).to_be_instance_of(six.text_type)
        expect(used_media[0]).to_equal(u'Тест.txt')