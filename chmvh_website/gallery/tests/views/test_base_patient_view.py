import pytest

from gallery.models import Patient
from gallery.views import BasePatientView


class TestBasePatientView(object):
    """Test cases for the base patient view"""

    @pytest.mark.django_db
    def test_context_no_patients(self):
        """Test the base view with no patients.

        If there are no patients, then `pet_categories` should be
        empty, and `in_memoriam` should be false.
        """
        view = BasePatientView()
        context = view.get_context_data()

        assert context['pet_categories'] == []
        assert not context['in_memoriam']

    @pytest.mark.django_db
    def test_context_pets(self, pets):
        """Test the base view with patients.

        If there are patients, `pet_categories` should be populated
        with the existing categories. `in_memoriam` should be `True` if
        there are any deceased patients and `False` otherwise.
        """
        view = BasePatientView()
        context = view.get_context_data()

        expected_categories = []
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if Patient.objects.filter(
                    deceased=False, first_letter=letter).exists():
                expected_categories.append(letter)

        expected_in_memoriam = Patient.objects.filter(deceased=True).exists()

        assert context['pet_categories'] == expected_categories
        assert context['in_memoriam'] == expected_in_memoriam
