from django.db.models.signals import post_save
from django.dispatch import receiver

from gallery.tasks import create_thumbnail, process_patient_picture


@receiver(post_save, sender='gallery.Patient')
def send_notifications(sender, instance, *args, **kwargs):
    """ Notify users that a reply has been posted """
    process_patient_picture.delay(instance)
