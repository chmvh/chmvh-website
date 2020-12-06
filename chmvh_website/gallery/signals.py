from django.db.models.signals import post_save
from django.dispatch import receiver

from gallery.tasks import process_patient_picture


@receiver(post_save, sender="gallery.Patient")
def process_picture(sender, instance, update_fields, *args, **kwargs):
    """
    Process a patients picture.

    This involves checking for different orientations as well as
    generating a thumbnail for the picture.

    Args:
        sender:
            The sender of the save event.
        instance:
            The Patient instance being saved.
        update_fields:
            The fields that were updated in the save.
        *args:
            Additional arguments.
        **kwargs:
            Additional keyword arguments.
    """
    if not update_fields or "thumbnail" not in update_fields:
        process_patient_picture(instance.id)
