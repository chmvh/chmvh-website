from django.core.management.base import BaseCommand

from gallery import models
from gallery.tasks import create_thumbnail


class Command(BaseCommand):
    help = 'Generates thumbnails for gallery images without thumbnails'

    def add_arguments(self, parser):
        parser.add_argument(
            '--overwrite',
            action='store_true',
            default=False,
            dest='overwrite',
            help='Generate thumbnails for all pictures.')

    def handle(self, *args, **kwargs):
        if kwargs['overwrite']:
            self.stdout.write(self.style.WARNING(
                'Overwriting previously generated thumbnails.'))

            patients = models.Patient.objects.all()
        else:
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
            if kwargs['overwrite'] and patient.thumbnail:
                patient.thumbnail.delete()

            create_thumbnail(patient)

        self.stdout.write(self.style.SUCCESS(
            "Successfully generated {}.".format(count_bit)))
