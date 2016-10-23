from django.db.models.signals import post_save
from django.dispatch import receiver

from gallery.tasks import create_thumbnail


@receiver(post_save, sender='gallery.Patient')
def send_notifications(sender, instance, update_fields, *args, **kwargs):
    """ Notify users that a reply has been posted """
    if not instance.thumbnail:
        if update_fields and 'thumbnail' not in update_fields:
            create_thumbnail(instance)
