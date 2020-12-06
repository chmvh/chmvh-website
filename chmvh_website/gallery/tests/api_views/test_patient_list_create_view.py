from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse

from rest_framework.test import APIRequestFactory

from gallery.api_views import PatientListCreateView
from gallery.models import Patient
from gallery.serializers import PatientSerializer


class TestPatientListCreateView(object):
    """Test cases for the patient list/create api view"""

    url = reverse("gallery:api:patient-list")

    def test_create_patient(
        self, admin_user: User, patient_info: dict, api_rf: APIRequestFactory
    ):
        """Test creating a new patient with a POST request.

        If valid data is POSTed to the view, a new patient should be
        created.
        """
        serializer = PatientSerializer(data=patient_info)
        assert serializer.is_valid()

        request = api_rf.post(self.url, patient_info)
        request.user = admin_user

        response = PatientListCreateView.as_view()(request)
        response.render()

        assert response.status_code == 201
        assert response.data == serializer.data

        assert Patient.objects.count() == 1

    def test_create_patient_invalid(
        self, admin_user: User, api_rf: APIRequestFactory
    ):
        """Test POSTing invalid data.

        If invalid data is submitted, the response should contain the
        errors.
        """
        data = {
            "first_name": "Spot",
            "last_name": "Barker",
        }
        expected = {
            "picture": ["No file was submitted."],
        }

        request = api_rf.post(self.url, data)
        request.user = admin_user

        response = PatientListCreateView.as_view()(request)
        response.render()

        assert response.status_code == 400
        assert response.data == expected

        assert Patient.objects.count() == 0

    def test_list_patients(
        self, admin_user: User, pet_factory, rf: RequestFactory
    ):
        """Test the patient list view with multiple patients.

        If there are multiple patients, they should be listed in of
        first and last name.
        """
        pet_factory(first_name="A", last_name="B")
        pet_factory(first_name="A", last_name="A")
        pet_factory(first_name="B", last_name="A")

        patients = Patient.objects.order_by("first_name", "last_name")
        serializer = PatientSerializer(patients, many=True)

        request = rf.get(self.url)
        request.user = admin_user
        response = PatientListCreateView.as_view()(request)
        response.render()

        assert response.status_code == 200

        assert response.data == serializer.data

    def test_no_patients(self, admin_user: User, rf: RequestFactory):
        """Test the view with no patients.

        If there are no patients, an empty list should be returned.
        """
        serializer = PatientSerializer(many=True)

        request = rf.get(self.url)
        request.user = admin_user
        response = PatientListCreateView.as_view()(request)
        response.render()

        assert response.status_code == 200

        assert response.data == serializer.data

    def test_unauthenticated(self, rf: RequestFactory):
        """Test the view with an unauthenticated user.

        If the request doesn't come from an authenticated user, the
        view should return a 401 status code.
        """
        request = rf.get(self.url)
        response = PatientListCreateView.as_view()(request)

        assert response.status_code == 401
