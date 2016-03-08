from django.db import models


class FieldsTestModel(models.Model):
    file_field = models.FileField(upload_to='test')
    image_field = models.ImageField(upload_to='test_image')
    char_field = models.CharField(max_length=255)
