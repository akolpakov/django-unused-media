from preggy import expect
from django.db import models

from django_unused_media.utils import get_file_fields, get_used_media
from .base import BaseTestCase
from .models import FileFieldsModel, CustomFileldsModel
from .utils import create_file, create_image


class UtilsTestCase(BaseTestCase):
    def setUp(self):
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
        file_fields = get_file_fields()
        expect(file_fields).to_be_instance_of(list).to_length(3)

        for f in file_fields:
            expect(f).to_be_instance_of(models.FileField)

        file_fields_names = [f.name for f in file_fields]

        expect(file_fields_names).to_include('file_field').to_include('image_field').to_include('custom_field')
        expect(file_fields_names).Not.to_include('char_field')

    def test_get_used_media(self):
        used_media = get_used_media()
        expect(used_media).to_be_instance_of(list).to_length(5)
