from django.db.models.signals import post_save
from django.dispatch import receiver

from gallery.tasks import create_thumbnail


@receiver(post_save, sender='gallery.Patient')
def send_notifications(sender, instance, created, *args, **kwargs):
    """ Notify users that a reply has been posted """
    if not instance.thumbnail:
        create_thumbnail(instance)
