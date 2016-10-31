from django.core.files.uploadedfile import SimpleUploadedFile

import pytest


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
