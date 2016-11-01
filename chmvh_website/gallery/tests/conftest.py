from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command

import pytest


@pytest.fixture(scope='function')
def featured_pets(db):
    """Populate the database with test data."""
    call_command('loaddata', 'gallery/tests/fixtures/featured-pets.json')


@pytest.fixture(scope='module')
def patient_info():
    image = SimpleUploadedFile(
        name='test_image.jpg',
        content=open(
            'gallery/tests/fixtures/images/test_picture.jpg', 'rb').read(),
        content_type='image/jpeg')

    return {
        'deceased': False,
        'description': 'Cool dog.',
        'featured': True,
        'first_name': 'Spot',
        'last_name': 'Barker',
        'picture': image,
    }


@pytest.fixture(scope='function')
def pets(db):
    """Populate the database with pet data"""
    call_command('loaddata', 'gallery/tests/fixtures/pets.json')
