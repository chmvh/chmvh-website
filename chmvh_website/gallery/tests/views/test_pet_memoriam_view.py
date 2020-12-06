import pytest
from django.test import RequestFactory
from django.urls import reverse

from gallery.views import BasePatientView, PetMemoriamView


class TestPetMemoriamView(object):
    """Test cases for the pet memoriam view"""

    @pytest.mark.django_db
    def test_filter_patients(self, pet_factory, rf: RequestFactory):
        """Test filtering patients by category.

        When this view is used, only deceased patients should be shown.
        """
        p1 = pet_factory(first_name="Fido", deceased=True)
        p2 = pet_factory(first_name="Jane", deceased=True)
        pet_factory(first_name="Gus")

        expected = [p1, p2]

        url = reverse("gallery:pet-memoriam")
        request = rf.get(url)
        response = PetMemoriamView.as_view()(request)

        assert response.status_code == 200
        assert list(response.context_data["pets"]) == expected

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
