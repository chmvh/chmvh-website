import pytest

from gallery.views import BasePatientView


@pytest.mark.django_db
def test_context_no_patients():
    """Test the base view with no patients.

    If there are no patients, then `pet_categories` should be
    empty, and `in_memoriam` should be false.
    """
    view = BasePatientView()
    context = view.get_context_data()

    assert context["pet_categories"] == []
    assert not context["in_memoriam"]


@pytest.mark.django_db
def test_context_letters(pet_factory):
    """
    There should be categories for each distinct first letter of
    patient names.
    """
    pet_factory(first_name="Spot")
    pet_factory(first_name="Fido")

    expected_categories = ["F", "S"]

    view = BasePatientView()
    context = view.get_context_data()

    assert context["pet_categories"] == expected_categories


@pytest.mark.django_db
def test_context_in_memoriam_no_deceased(pet_factory):
    """
    With no deceased patients, the "in_memoriam" context should be
    ``False``.
    """
    pet_factory(first_name="Fluffy")

    view = BasePatientView()
    context = view.get_context_data()

    assert not context["in_memoriam"]


@pytest.mark.django_db
def test_context_in_memoriam_with_deceased(pet_factory):
    """
    With deceased patients, the "in_memoriam" context should be
    ``True``.
    """
    pet_factory(first_name="Fluffy", deceased=True)

    view = BasePatientView()
    context = view.get_context_data()

    assert context["in_memoriam"]
