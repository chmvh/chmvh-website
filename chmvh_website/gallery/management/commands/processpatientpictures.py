from django.core.management.base import BaseCommand

from tqdm import tqdm

from gallery import models
from gallery.tasks import process_patient_picture


class Command(BaseCommand):
    help = 'Processes patient pictures.'

    def handle(self, *args, **kwargs):
        count = models.Patient.objects.all().count()
        if count == 0:
            self.stdout.write("No patients to process.")

            return
        elif count == 1:
            count_bit = '1 patient'
        else:
            count_bit = '{0} patients'.format(count)

        self.stdout.write('Processing {}...'.format(count_bit))

        successes = 0

        for patient in tqdm(models.Patient.objects.all()):
            if process_patient_picture(patient.id):
                successes += 1

        self.stdout.write(self.style.SUCCESS(
            "Successfully processed {0} of {1} patient pictures".format(
                successes, count)))
