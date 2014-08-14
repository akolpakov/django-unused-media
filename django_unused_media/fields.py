from django.db import models
import logging

logger = logging.getLogger(__name__)


def cleanup_field(field):
    if not isinstance(field, models.FileField):
        raise Exception('Could not cleanup field %s. It is not FileField' % field)

    try:
        logging.info('We going to remove media file %s from the field %s' % (field.file, field))
        field.delete(save=False)
    except Exception as e:
        logging.error('Could not cleanup field %s. %s' % (field, e))