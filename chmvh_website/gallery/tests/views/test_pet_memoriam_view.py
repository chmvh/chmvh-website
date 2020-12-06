from django.test import RequestFactory
from django.urls import reverse

import pytest

from gallery.models import Patient
from gallery.views import BasePatientView, PetMemoriamView


class TestPetMemoriamView(object):
    """Test cases for the pet memoriam view"""

    @pytest.mark.django_db
    def test_filter_patients(self, pets, rf: RequestFactory):
        """Test filtering patients by category.

        When this view is used, only deceased patients should be shown.
        """
        url = reverse("gallery:pet-memoriam")
        request = rf.get(url)
        response = PetMemoriamView.as_view()(request)

        expected = Patient.objects.filter(deceased=True)

        assert response.status_code == 200

        base_context = BasePatientView().get_context_data()
        assert base_context.items() <= response.context_data.items()

        assert list(response.context_data["pets"]) == list(expected)

    @pytest.mark.django_db
    def test_no_patients(self, rf: RequestFactory):
        """Test the view with no patients.

        If there are no patients, the `pets` list should be empty.
        """
        url = reverse("gallery:pet-memoriam")
        request = rf.get(url)
        response = PetMemoriamView.as_view()(request)

        assert response.status_code == 200
        assert "gallery/pet-list.html" in response.template_name

        base_context = BasePatientView().get_context_data()
        assert base_context.items() <= response.context_data.items()

        assert response.context_data["category"] == "In Memoriam"
        assert list(response.context_data["pets"]) == []
