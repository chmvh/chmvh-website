from django.core.management.base import BaseCommand

from gallery import models
from gallery.tasks import create_thumbnail


class Command(BaseCommand):
    help = 'Generates thumbnails for the gallery images'

    def handle(self, *args, **kwargs):
        patients = models.Patient.objects.filter(thumbnail=None)

        count = patients.count()
        if count == 0:
            self.stdout.write("No thumbnails to generate.")

            return
        elif count == 1:
            count_bit = '1 thumbnail'
        else:
            count_bit = '{0} thumbnails'.format(count)

        self.stdout.write('Generating {}...'.format(count_bit))

        for patient in patients:
            create_thumbnail(patient)

        self.stdout.write(self.style.SUCCESS(
            "Successfully generated {}.".format(count_bit)))
