import pytest

from django.core.management import call_command

from gallery.testing_utils import get_test_picture


@pytest.fixture(scope='function')
def featured_pets(db):
    """Populate the database with test data."""
    call_command('loaddata', 'gallery/tests/fixtures/featured-pets.json')


@pytest.fixture(scope='module')
def patient_info():
    return {
        'deceased': False,
        'description': 'Cool dog.',
        'featured': True,
        'first_name': 'Spot',
        'last_name': 'Barker',
        'picture': get_test_picture(),
    }


@pytest.fixture(scope='function')
def pets(db):
    """Populate the database with pet data"""
    call_command('loaddata', 'gallery/tests/fixtures/pets.json')
