import pytest

from gallery.models import Patient


class TestPatientModel(object):
    """Test cases for the patient model"""

    @pytest.mark.django_db
    def test_create_with_all_fields(self, patient_info):
        """Test creating a patient with all fields specified"""
        patient = Patient.objects.create(**patient_info)

        assert patient.deceased == patient_info["deceased"]
        assert patient.description == patient_info["description"]
        assert patient.featured == patient_info["featured"]
        assert patient.first_letter == patient_info["first_name"][0]
        assert patient.first_name == patient_info["first_name"]
        assert patient.last_name == patient_info["last_name"]

    @pytest.mark.django_db
    def test_first_letter_update(self, patient_info):
        """Test updating the `first_letter` field on save.

        When a patient instance is saved, its `first_letter` attribute
        should be updated."""
        patient = Patient.objects.create(**patient_info)

        assert patient.first_letter != "F"

        patient.first_name = "Fido"
        patient.save()
        patient.refresh_from_db()

        assert patient.first_letter == "F"

    @pytest.mark.django_db
    def test_ordering(self, pet_factory):
        """Test the ordering of patient instances.

        Patients should be ordered by first name, then last name.
        """
        p1 = pet_factory(first_name="B")
        p2 = pet_factory(first_name="A", last_name="A")
        p3 = pet_factory(first_name="A", last_name="B")

        patients = [p2, p3, p1]

        assert list(Patient.objects.all()) == patients

    def test_string_conversion(self):
        """Test converting a Patient instance to a string.

        The resulting string should contain the patient's name.
        """
        patient = Patient(first_name="Spot", last_name="Barker")

        assert str(patient) == "{first} {last}".format(
            first=patient.first_name, last=patient.last_name
        )

    def test_string_conversion_first_name_only(self):
        """Test the string conversion of a patient with no last name.

        The resulting string should have the patient's first name.
        """
        patient = Patient(first_name="Spot")

        assert str(patient) == patient.first_name
