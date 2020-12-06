import pathlib

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from gallery import models


def create_patient(
    first_name: str = "Spot",
    last_name: str = "Barker",
    deceased: bool = False,
    description: str = "",
    featured: bool = False,
    picture: File = None,
) -> models.Patient:
    """
    Create a patient for testing purposes.

    If a required field is omitted, a default value will be provided.

    Args:
        first_name:
            The patient's first name. Defaults to `Spot`.
        last_name:
            The patient's last name. Defaults to `Barker`.
        deceased:
            A boolean indicating if the patient is deceased. Defaults
            to `False`.
        description:
            The patient's description.
        featured:
            A boolean indicating if the patient is featured. Defaults
            to `False`.
        picture:
            The patient's picture. Defaults to a 1x1 blank picture.

    Returns:
        A new `Patient` instance with the supplied attributes.
    """
    patient_info = {
        "first_name": first_name,
        "last_name": last_name,
        "deceased": deceased,
        "description": description,
        "featured": featured,
        "picture": picture or get_test_picture(),
    }

    return models.Patient.objects.create(**patient_info)


def get_test_picture() -> SimpleUploadedFile:
    """
    Get a picture for testing.

    The picture is 1x1 with a single white pixel.

    Returns:
        A file whose contents are the sample image described.
    """
    current_dir = pathlib.Path(__file__).parent
    src = current_dir / "tests" / "fixtures" / "images" / "test_picture.jpg"

    return SimpleUploadedFile(
        content=open(src, "rb").read(),
        content_type="image/jpeg",
        name="test_image.jpg",
    )
