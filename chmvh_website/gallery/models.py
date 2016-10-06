from django.db import models


def patient_image_path(instance, filename):
    """Generate the path to save a patient's image under.

    Args:
        instance (obj):
            The Patient instance that the file field belongs to.
        filename (str):
            The orignal filename of the uploaded image.

    Returns:
        str:
            The file path to upload the provided image to.
    """
    path = 'patients/{0}/{1}'.format(
        instance.first_name[0], instance.first_name, instance.last_name)

    if instance.last_name:
        path = '{0} {1}'.format(path, instance.last_name)

    return path


class Patient(models.Model):
    """A veterinary patient with a name and picture."""
    deceased = models.BooleanField(
        default=False,
        help_text=("Patients marked as deceased will have their picture "
                   "displayed in the 'In Memoriam' section."),
        verbose_name='deceased')
    first_name = models.CharField(
        max_length=100,
        verbose_name='first name')
    last_name = models.CharField(
        blank=True,
        help_text=("This is only used to identify the patient, and is not "
                   "displayed publicly."),
        max_length=100,
        verbose_name='last name')
    picture = models.ImageField(
        height_field='picture_height',
        upload_to=patient_image_path,
        verbose_name='picture',
        width_field='picture_width')
