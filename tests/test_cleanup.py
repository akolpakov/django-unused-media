# -*- coding: utf-8 -*-
import os
import sys

import six
from django.db import models
from django_unused_media.cleanup import _get_file_fields, _get_all_media, \
    get_used_media, get_unused_media, _remove_media, remove_unused_media, remove_empty_dirs, MEDIA_ROOT
from preggy import expect

from .base import BaseTestCase
from .models import FileFieldsModel, CustomFileldsModel
from .utils import create_file, create_image, create_file_and_write, exists_media_path

_ver = sys.version_info


class TestCleanup(BaseTestCase):
    def setUp(self):
        super(TestCleanup, self).setUp()

        self.model1 = FileFieldsModel.objects.create(
            file_field=create_file('file1.txt'),
            image_field=create_image('image1.jpg'),
            char_field='test1'
        )

        self.model2 = FileFieldsModel.objects.create(
            file_field=create_file('file2.txt'),
            image_field=create_image('image2.jpg'),
            char_field='test2'
        )

        self.model3 = CustomFileldsModel.objects.create(
            custom_field=create_file('file3.txt'),
            char_field='test3'
        )

        self.model4 = CustomFileldsModel.objects.create(
            char_field='test4'
        )

    @staticmethod
    def __make_abs_path(path):
        return os.path.join(MEDIA_ROOT, path)

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
            .to_include(self.model1.file_field.path)\
            .to_include(self.model1.image_field.path)\
            .to_include(self.model2.file_field.path)\
            .to_include(self.model2.image_field.path)\
            .to_include(self.model3.custom_field.path)

    def test_get_all_media(self):
        expect(_get_all_media())\
            .to_be_instance_of(list).to_length(5)\
            .to_include(self.model1.file_field.path)\
            .to_include(self.model1.image_field.path)\
            .to_include(self.model2.file_field.path)\
            .to_include(self.model2.image_field.path)\
            .to_include(self.model3.custom_field.path)

    def test_get_all_media_with_additional(self):
        create_file_and_write(u'file.txt')
        expect(_get_all_media())\
            .to_be_instance_of(list).to_length(6)\
            .to_include(self.model1.file_field.path)\
            .to_include(self.model1.image_field.path)\
            .to_include(self.model2.file_field.path)\
            .to_include(self.model2.image_field.path)\
            .to_include(self.model3.custom_field.path)\
            .to_include(self.__make_abs_path(u'file.txt'))

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
            .to_include(self.model1.file_field.path)\
            .to_include(self.model1.image_field.path)\
            .to_include(self.model2.file_field.path)\
            .to_include(self.model2.image_field.path)\
            .to_include(self.model3.custom_field.path)\
            .to_include(self.__make_abs_path(u'file.txt'))\
            .Not.to_include(self.__make_abs_path(u'.file2.txt'))\
            .Not.to_include(self.__make_abs_path(u'test.txt'))\
            .to_include(self.__make_abs_path(u'do_not_exclude/test.txt'))

    def test_get_all_media_with_exclude_folder(self):
        create_file_and_write(u'exclude_dir/file1.txt')
        create_file_and_write(u'exclude_dir/file2.txt')
        create_file_and_write(u'file3.txt')
        expect(_get_all_media(['exclude_dir/*']))\
            .to_be_instance_of(list).to_length(6)\
            .to_include(self.model1.file_field.path)\
            .to_include(self.model1.image_field.path)\
            .to_include(self.model2.file_field.path)\
            .to_include(self.model2.image_field.path)\
            .to_include(self.model3.custom_field.path)\
            .to_include(self.__make_abs_path(u'file3.txt'))\
            .Not.to_include(self.__make_abs_path(u'exclude_dir/file1.txt'))\
            .Not.to_include(self.__make_abs_path(u'exclude_dir/file2.txt'))

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

    def test_ascii_filenames(self):
        create_file_and_write(u'Тест.txt')
        used_media = get_unused_media()
        expect(used_media).to_be_instance_of(list).to_length(1)
        expect(used_media[0]).to_be_instance_of(six.text_type)
        expect(used_media[0]).to_equal(self.__make_abs_path(u'Тест.txt'))

    def test_relative_path(self):
        FileFieldsModel.objects.create(
            file_field='./test_rel_path/file1.txt',
        )
        expect(get_used_media()) \
            .to_be_instance_of(list)\
            .to_include(self.__make_abs_path('test_rel_path/file1.txt'))
