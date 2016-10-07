from django.views import generic

from gallery import models


ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class GalleryIndexView(generic.base.TemplateView):
    template_name = 'gallery/index.html'

    def get_context_data(self):
        context = super(GalleryIndexView, self).get_context_data()

        patient_letters = []
        for letter in ALPHABET:
            if models.Patient.objects.filter(first_letter=letter).exists():
                patient_letters.append(letter)
        context['patient_letters'] = patient_letters

        return context
