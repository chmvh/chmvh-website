from functools import reduce

from django.db.models import Q
from django.views import generic

from gallery import models


ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def patient_context():
    context = {}

    categories = []
    for letter in ALPHABET:
        if models.Patient.objects.filter(first_letter=letter).exists():
            categories.append(letter)
    context['pet_categories'] = categories

    context['in_memoriam'] = models.Patient.objects.filter(
        deceased=True).exists()

    return context


class GalleryIndexView(generic.base.TemplateView):
    template_name = 'gallery/index.html'

    def get_context_data(self):
        context = super(GalleryIndexView, self).get_context_data()

        context.update(patient_context())

        featured = models.Patient.objects.filter(featured=True)
        context['featured_pets'] = featured

        return context


class PetListView(generic.base.TemplateView):
    template_name = 'gallery/pet-list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PetListView, self).get_context_data(*args, **kwargs)

        letter = self.kwargs.get('first_letter').upper()
        context['category'] = letter

        pets = models.Patient.objects.filter(
            first_letter__iexact=letter).exclude(
            deceased=True)
        context['pets'] = pets

        context.update(patient_context())

        return context


class PetMemoriamView(generic.base.TemplateView):
    template_name = 'gallery/pet-list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PetMemoriamView, self).get_context_data(
            *args, **kwargs)

        context['category'] = 'In Memoriam'

        pets = models.Patient.objects.filter(deceased=True)
        context['pets'] = pets

        context.update(patient_context())

        return context


class PetSearchView(generic.base.TemplateView):
    template_name = 'gallery/search.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PetSearchView, self).get_context_data(*args, **kwargs)

        context.update(patient_context())

        query = self.request.GET.get('q')
        context['query'] = query

        pets = models.Patient.objects.filter(
            reduce(
                lambda q, f: q & Q(first_name__icontains=f),
                query.split(),
                Q()))
        context['pets'] = pets

        return context
