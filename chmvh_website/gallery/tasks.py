from io import BytesIO

from celery.utils.log import get_task_logger

from django.conf import settings
from django.core.files.base import ContentFile

from PIL import ExifTags, Image

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
        logger.warning(_INVALID_FORMAT_ERROR.format(
            path=patient.picture.path,
            type=pil_type))

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


@celery_app.task
def process_patient_picture(patient, logger=default_logger):
    """
    Process
    Args:
        patient:
            The patient whose image to process.
        logger:
            The logger to use for the function.
    """
    logger.debug("Processing {file_path}".format(
        file_path=patient.picture.path))

    image = Image.open(patient.picture.path)

    pil_type = image.format
    if pil_type in ('JPEG', 'MPO'):
        pil_type = 'JPEG'   # Saving it as a jpeg makes it easier to process
    else:
        # No need to process any other files
        return

    orientation_key = None

    for key in ExifTags.TAGS.keys():
        if ExifTags.TAGS[key] == 'Orientation':
            orientation_key = key
            break

    if orientation_key is None:
        logger.warning("No orientation key was found, not rotating.")
    else:
        if hasattr(image, '_getexif') and image._getexif() is not None:
            exif = dict(image._getexif().items())
            orientation = exif.get(orientation_key)

            logger.debug(
                "Current picture has orientation {0}".format(orientation))

            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)

    image.save(patient.picture.path, pil_type)

    if not patient.thumbnail:
        create_thumbnail.delay(patient)

    return True
