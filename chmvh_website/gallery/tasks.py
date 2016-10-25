from io import BytesIO

from celery.utils.log import get_task_logger

from django.conf import settings
from django.core.files.base import ContentFile

from PIL import Image

from chmvh_website import celery_app


_INVALID_FORMAT_ERROR = ("Can't generate thumbnail for {type} filetype. "
                         "(Path: {path})")


default_logger = get_task_logger(__name__)


@celery_app.task
def create_thumbnail(patient, logger=default_logger):
    logger.debug("Generating thumbnail for {0}".format(patient.picture.path))
    image = Image.open(patient.picture.path)

    pil_type = image.format
    if pil_type == 'JPEG':
        ext = 'jpg'
    elif pil_type == 'PNG':
        ext = 'png'
    else:
        logger.warning(_INVALID_FORMAT_ERROR.format({
            'path': patient.picture.path,
            'type': pil_type,
        }))

        return False

    image.thumbnail(settings.GALLERY_THUMBNAIL_SIZE)

    temp_handle = BytesIO()
    image.save(temp_handle, pil_type)
    temp_handle.seek(0)

    path = patient.picture.name.rsplit('.', 1)[0]
    thumb_path = '{0}_thumbnail.{1}'.format(path, ext)
    patient.thumbnail.save(
        thumb_path,
        ContentFile(temp_handle.getvalue()),
        save=False)

    logger.debug("Saving thumbnail to {0}".format(thumb_path))
    patient.save(update_fields=['thumbnail'])

    logger.info("Generated thumbnail {0}".format(thumb_path))

    return True
