# -*- coding: utf-8 -*-

import six
import mock

from preggy import expect
from django.db import models

from django_unused_media.cleanup import get_file_fields, get_all_media, get_used_media, \
    get_unused_media, remove_unused_media
from django_unused_media.remove import remove_media, remove_empty_dirs
from .base import BaseTestCase
from .models import FileFieldsModel, CustomFileldsModel, CustomManagerModel


def win_os_walk(path):
    yield 'C:/dir', None, [r'test\file.txt']      # Windows walk returns mixed slashes in list of files


def win_os_abspath(path):
    return path.replace('/', '\\')


class TestCleanup(BaseTestCase):
    def setUp(self):
        super(TestCleanup, self).setUp()

        self.model1 = FileFieldsModel.objects.create(
            file_field=self._create_file('file1.txt'),
            image_field=self._create_image('image1.jpg'),
            char_field='test1'
        )

        self.model2 = FileFieldsModel.objects.create(
            file_field=self._create_file('file2.txt'),
            image_field=self._create_image('image2.jpg'),
            char_field='test2'
        )

        self.model3 = CustomFileldsModel.objects.create(
            custom_field=self._create_file('file3.txt'),
            char_field='test3'
        )

        self.model4 = CustomFileldsModel.objects.create(
            char_field='test4'
        )

    def test_get_file_fields(self):
        file_fields = get_file_fields()
        expect(file_fields).to_be_instance_of(list).to_length(4)

        for f in file_fields:
            expect(f).to_be_instance_of(models.FileField)

        file_fields_names = [f.name for f in file_fields]

        expect(file_fields_names)\
            .to_include('file_field')\
            .to_include('image_field')\
            .to_include('custom_field')
        expect(file_fields_names).Not.to_include('char_field')
        expect(file_fields_names).Not.to_include('active')

    def test_get_used_media(self):
        expect(get_used_media())\
            .to_be_instance_of(set).to_length(5)\
            .to_include(self.model1.file_field.path)\
            .to_include(self.model1.image_field.path)\
            .to_include(self.model2.file_field.path)\
            .to_include(self.model2.image_field.path)\
            .to_include(self.model3.custom_field.path)

    def test_get_all_media(self):
        expect(get_all_media())\
            .to_be_instance_of(set).to_length(5)\
            .to_include(self.model1.file_field.path)\
            .to_include(self.model1.image_field.path)\
            .to_include(self.model2.file_field.path)\
            .to_include(self.model2.image_field.path)\
            .to_include(self.model3.custom_field.path)

    def test_get_all_media_with_additional(self):
        self._media_create(u'file.txt')
        expect(get_all_media())\
            .to_be_instance_of(set).to_length(6)\
            .to_include(self.model1.file_field.path)\
            .to_include(self.model1.image_field.path)\
            .to_include(self.model2.file_field.path)\
            .to_include(self.model2.image_field.path)\
            .to_include(self.model3.custom_field.path)\
            .to_include(self._media_abs_path(u'file.txt'))

    def test_get_all_media_with_exclude(self):
        self._media_create(u'file.txt')
        self._media_create(u'.file2.txt')
        self._media_create(u'test.txt')
        self._media_create(u'do_not_exclude/test.txt')
        self._media_create(u'one.png')
        self._media_create(u'two.png')
        self._media_create(u'three.png')
        expect(get_all_media(['.*', '*.png', 'test.txt']))\
            .to_be_instance_of(set).to_length(7)\
            .to_include(self.model1.file_field.path)\
            .to_include(self.model1.image_field.path)\
            .to_include(self.model2.file_field.path)\
            .to_include(self.model2.image_field.path)\
            .to_include(self.model3.custom_field.path)\
            .to_include(self._media_abs_path(u'file.txt'))\
            .Not.to_include(self._media_abs_path(u'.file2.txt'))\
            .Not.to_include(self._media_abs_path(u'test.txt'))\
            .to_include(self._media_abs_path(u'do_not_exclude/test.txt'))

    def test_get_all_media_with_exclude_folder(self):
        self._media_create(u'exclude_dir/file1.txt')
        self._media_create(u'exclude_dir/file2.txt')
        self._media_create(u'file3.txt')
        expect(get_all_media(['exclude_dir/*']))\
            .to_be_instance_of(set).to_length(6)\
            .to_include(self.model1.file_field.path)\
            .to_include(self.model1.image_field.path)\
            .to_include(self.model2.file_field.path)\
            .to_include(self.model2.image_field.path)\
            .to_include(self.model3.custom_field.path)\
            .to_include(self._media_abs_path(u'file3.txt'))\
            .Not.to_include(self._media_abs_path(u'exclude_dir/file1.txt'))\
            .Not.to_include(self._media_abs_path(u'exclude_dir/file2.txt'))

    def test_get_all_media_with_minimum_file_age(self):
        self._media_create(u'fresh_file.txt')
        expect(get_all_media(minimum_file_age=60)) \
            .to_be_instance_of(set).to_length(0)

    def test_get_all_media_with_minimum_file_age_2(self):
        self._media_create(u'fresh_file.txt', file_age=70)
        expect(get_all_media(minimum_file_age=60)) \
            .to_be_instance_of(set).to_length(1) \
            .to_include(self._media_abs_path(u'fresh_file.txt'))

    @mock.patch('django_unused_media.cleanup.os.path.abspath', side_effect=win_os_abspath)
    @mock.patch('django_unused_media.cleanup.os.walk', side_effect=win_os_walk)
    def test_get_all_media_win(self, mock_walk, mock_abspath):
        expect(get_all_media())\
               .to_be_instance_of(set).to_length(1)\
               .to_include(r'C:\dir\test\file.txt')

    def test_get_unused_media_empty(self):
        expect(get_unused_media()).to_be_empty()

    def test_get_unused_media(self):
        self._media_create(u'notused.txt')
        used_media = get_unused_media()
        expect(used_media).to_be_instance_of(set).to_length(1)
        expect(next(iter(used_media))).to_match(r'^.*notused.txt')

    def test_get_unused_media_subfolder(self):
        self._media_create(u'subfolder/notused.txt')
        used_media = get_unused_media()
        expect(used_media).to_be_instance_of(set).to_length(1)
        expect(next(iter(used_media))).to_match(r'^.*subfolder/notused.txt$')

    def test_remove_media(self):
        expect(self._media_exists(u'file.txt')).to_be_false()
        self._media_create(u'file.txt')
        expect(self._media_exists(u'file.txt')).to_be_true()
        remove_media([u'file.txt'])
        expect(self._media_exists(u'file.txt')).to_be_false()

    def test_remove_unused_media(self):
        expect(get_unused_media()).to_be_empty()
        self._media_create(u'notused.txt')
        expect(get_unused_media()).Not.to_be_empty()
        remove_unused_media()
        expect(get_unused_media()).to_be_empty()

    def test_remove_empty_dirs(self):
        self._media_create(u'sub1/sub2/sub3/notused.txt')
        remove_unused_media()
        remove_empty_dirs()
        expect(self._media_exists(u'sub1/sub2/sub3/notused.txt')).to_be_false()
        expect(self._media_exists(u'sub1/sub2/sub3')).to_be_false()
        expect(self._media_exists(u'sub1/sub2')).to_be_false()
        expect(self._media_exists(u'sub1')).to_be_false()

    def test_remove_empty_dirs_not_empty(self):
        self._media_create(u'sub1/sub2/sub3/notused.txt')
        remove_empty_dirs()
        expect(self._media_exists(u'sub1/sub2/sub3/notused.txt')).to_be_true()
        expect(self._media_exists(u'sub1/sub2/sub3')).to_be_true()
        expect(self._media_exists(u'sub1/sub2')).to_be_true()
        expect(self._media_exists(u'sub1')).to_be_true()

    def test_ascii_filenames(self):
        self._media_create(u'Тест.txt')
        used_media = get_unused_media()
        expect(used_media).to_be_instance_of(set).to_length(1)
        expect(next(iter(used_media))).to_be_instance_of(six.text_type)
        expect(next(iter(used_media))).to_equal(self._media_abs_path(u'Тест.txt'))

    def test_relative_path(self):
        FileFieldsModel.objects.create(
            file_field='./test_rel_path/file1.txt',
        )
        expect(get_used_media()) \
            .to_be_instance_of(set)\
            .to_include(self._media_abs_path('test_rel_path/file1.txt'))

    def test_custom_manager(self):
        model_active = CustomManagerModel.objects.create(
            active=True,
            file_field=self._create_file('file_custom_1.txt'),
        )
        model_not_active = CustomManagerModel.objects.create(
            active=False,
            file_field=self._create_file('file_custom_2.txt'),
        )

        expect(get_used_media()) \
            .to_be_instance_of(set) \
            .to_include(model_active.file_field.path) \
            .to_include(model_not_active.file_field.path)
