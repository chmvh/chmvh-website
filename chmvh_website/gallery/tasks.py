from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile

from PIL import Image

from chmvh_website import celery_app


@celery_app.task
def create_thumbnail(patient):
    image = Image.open(patient.picture.path)

    pil_type = image.format
    if pil_type == 'JPEG':
        ext = 'jpg'
    elif pil_type == 'PNG':
        ext = 'png'

    image.thumbnail(settings.GALLERY_THUMBNAIL_SIZE)

    temp_handle = BytesIO()
    image.save(temp_handle, pil_type)
    temp_handle.seek(0)

    path = patient.picture.name.rsplit('.', 1)[0]
    patient.thumbnail.save(
        '{0}_thumbnail.{1}'.format(path, ext),
        ContentFile(temp_handle.getvalue()),
        save=False)

    patient.save(update_fields=['thumbnail'])
