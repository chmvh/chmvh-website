from django.test import RequestFactory
from django.urls import reverse

import pytest

from gallery.models import Patient
from gallery.views import BasePatientView, PetListView


class TestPetListView(object):
    """Test cases for the pet list view"""

    @pytest.mark.django_db
    def test_filter_patients(self, pets, rf: RequestFactory):
        """Test filtering patients by category.

        When a category is viewed, only patients in that category
        should be displayed.
        """
        url = reverse("gallery:pet-list", kwargs={"first_letter": "A"})
        request = rf.get(url)
        response = PetListView.as_view()(request, first_letter="A")

        expected = Patient.objects.filter(deceased=False, first_letter="A")

        assert response.status_code == 200

        base_context = BasePatientView().get_context_data()
        assert base_context.items() <= response.context_data.items()

        assert list(response.context_data["pets"]) == list(expected)

    @pytest.mark.django_db
    def test_no_patients(self, rf: RequestFactory):
        """Test the view with no patients.

        If there are no patients in the given category, the `pets`
        variable should be an empty list.
        """
        url = reverse("gallery:pet-list", kwargs={"first_letter": "A"})
        request = rf.get(url)
        response = PetListView.as_view()(request, first_letter="A")

        assert response.status_code == 200
        assert "gallery/pet-list.html" in response.template_name

        base_context = BasePatientView().get_context_data()
        assert base_context.items() <= response.context_data.items()

        assert response.context_data["category"] == "A"
        assert list(response.context_data["pets"]) == []
