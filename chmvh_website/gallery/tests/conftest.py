import factory
import pytest

from gallery.testing_utils import get_test_picture


@pytest.fixture(scope="module")
def patient_info():
    return {
        "deceased": False,
        "description": "Cool dog.",
        "featured": True,
        "first_name": "Spot",
        "last_name": "Barker",
        "picture": get_test_picture(),
    }


class PetFactory(factory.django.DjangoModelFactory):
    picture = factory.django.ImageField()

    class Meta:
        model = "gallery.Patient"


@pytest.fixture
def pet_factory(db):
    return PetFactory
