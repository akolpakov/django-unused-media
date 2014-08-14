from models import FieldsTestModel
from utils import create_image, create_file
from django_unused_media.fields import cleanup_field
from test_base import BaseTestCase


class FieldsTestCase(BaseTestCase):
    def setUp(self):
        self.model = FieldsTestModel(
            file_field=create_file('file.txt'),
            image_field=create_image('image.jpg'),
            char_field='test'
        )
        self.model.save()

    def tearDown(self):
        FieldsTestModel.objects.all().delete()

    def test_setup(self):
        """Check properly setup of test environment"""
        # TODO
        pass

    def test_non_file_field(self):
        """Try to cleanup field which is not FileField should throw exception"""
        with self.assertRaises(Exception):
            cleanup_field(self.model.char_field)

    def test_file_field(self):
        """Try to cleanup FileField"""
        # TODO
        pass

    def test_image_field(self):
        """Try to cleanup ImageField"""
        # TODO
        pass

    def test_file_field_subclass(self):
        """Try to cleanup subclass"""
        # TODO
        pass

    def test_file_not_exists(self):
        """Try to cleanup Field which refer to non existence media"""
        # TODO
        pass

    # TODO Test different storage
