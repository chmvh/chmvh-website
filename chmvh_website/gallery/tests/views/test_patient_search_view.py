from unittest import mock

from django.test import RequestFactory
from django.urls import reverse

import pytest

from gallery.testing_utils import create_patient
from gallery.views import PatientSearchView


class TestPatientSearchView(object):
    """Test cases for the patient search view"""
    url = reverse('gallery:search')

    @pytest.mark.django_db
    def test_initial_get(self, rf: RequestFactory):
        """Test the initial GET request to the view.

        The initial request should display a blank search form, and it
        should not hit the database.
        """
        request = rf.get(self.url)
        response = PatientSearchView.as_view()(request)

        assert response.status_code == 200
        assert 'gallery/search.html' in response.template_name

        assert not response.context_data['query']
        assert response.context_data['pets'] == []

    @pytest.mark.django_db
    def test_search(self, rf: RequestFactory):
        """Test searching for a query string.

        Searching by name should return patients whose first name
        starts with the given query.
        """
        p1 = create_patient('Adam')
        p2 = create_patient('ada')
        create_patient('foo', 'adams')

        expected = [p1, p2]

        request = rf.get(self.url, {'q': 'ada'})
        response = PatientSearchView.as_view()(request)

        assert response.status_code == 200

        assert response.context_data['query'] == 'ada'
        assert list(response.context_data['pets']) == expected
