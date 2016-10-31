import pytest

from gallery.models import Patient
from gallery.serializers import PatientSerializer


class TestPatientSerializer(object):
    """Test cases for the patient serializer"""

    @pytest.mark.django_db
    def test_deserialize(self, patient_info):
        """Test deserializing a patient instance.

        The serializer should be able to take serialized data and
        construct a patient instance from it.
        """
        serializer = PatientSerializer(data=patient_info)

        assert serializer.is_valid(), serializer.errors

        patient = serializer.save()

        assert patient.first_name == patient_info['first_name']
        assert patient.last_name == patient_info['last_name']
        assert patient.featured == patient_info['featured']
        assert patient.deceased == patient_info['deceased']

    @pytest.mark.django_db
    def test_serialize(self, patient_info):
        """Test serializing a patient object.

        Serializing a patient should return info about that patient,
        but not the patient's picture.
        """
        patient = Patient.objects.create(**patient_info)
        serializer = PatientSerializer(patient)

        expected = {
            'first_name': patient_info['first_name'],
            'last_name': patient_info['last_name'],
            'featured': patient_info['featured'],
            'deceased': patient_info['deceased'],
        }

        assert serializer.data == expected
