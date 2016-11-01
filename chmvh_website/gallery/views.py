from functools import reduce
import string

from django.db.models import Q
from django.views import generic

from gallery import models


class BasePatientView(object):
    """Responsible for generating basic patient context data"""

    def get_context_data(self) -> dict:
        """
        Get context data about patients.

        Specifically, this method adds context about existing patient
        categories.

        Returns:
            Context about existing `Patient` instances.
        """
        context = dict()

        context['in_memoriam'] = models.Patient.objects.filter(
            deceased=True).exists()

        categories = []
        for letter in string.ascii_uppercase:
            if models.Patient.objects.filter(
                    deceased=False, first_letter=letter).exists():
                categories.append(letter)
        context['pet_categories'] = categories

        return context


class GalleryIndexView(BasePatientView, generic.base.TemplateView):
    template_name = 'gallery/index.html'

    def get_context_data(self):
        context = super(GalleryIndexView, self).get_context_data()

        featured = models.Patient.objects.filter(featured=True)
        context['featured_pets'] = featured

        return context


class PetListView(BasePatientView, generic.base.TemplateView):
    template_name = 'gallery/pet-list.html'

    def get_context_data(self, first_letter, *args, **kwargs):
        context = super(PetListView, self).get_context_data(*args, **kwargs)

        letter = first_letter.upper()
        context['category'] = letter

        pets = models.Patient.objects.filter(
            first_letter__iexact=letter).exclude(
            deceased=True)
        context['pets'] = pets

        return context


class PetMemoriamView(BasePatientView, generic.base.TemplateView):
    template_name = 'gallery/pet-list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PetMemoriamView, self).get_context_data(
            *args, **kwargs)

        context['category'] = 'In Memoriam'

        pets = models.Patient.objects.filter(deceased=True)
        context['pets'] = pets

        return context


class PetSearchView(BasePatientView, generic.base.TemplateView):
    template_name = 'gallery/search.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PetSearchView, self).get_context_data(*args, **kwargs)

        query = self.request.GET.get('q')
        context['query'] = query

        pets = models.Patient.objects.filter(
            reduce(
                lambda q, f: q & Q(first_name__icontains=f),
                query.split(),
                Q()))
        context['pets'] = pets

        return context
