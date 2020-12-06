from django.test import RequestFactory
from django.urls import reverse

import pytest

from gallery.models import Patient
from gallery.views import GalleryIndexView


class TestGalleryIndexView(object):
    """Test cases for the gallery index view"""

    url = reverse("gallery:index")

    @pytest.mark.django_db
    def test_featured_pets(self, featured_pets, rf: RequestFactory):
        """Test the index view with featured pets.

        If there are featured pets, they should be passed to the index
        view.
        """
        request = rf.get(self.url)
        response = GalleryIndexView.as_view()(request)

        expected = list(Patient.objects.filter(featured=True))

        assert response.status_code == 200
        assert list(response.context_data["featured_pets"]) == expected

    @pytest.mark.django_db
    def test_no_featured_pets(self, rf: RequestFactory):
        """Test the index view with no featured pets.

        If there are no featured pets, then the featured pets context
        should be empty.
        """
        request = rf.get(self.url)
        response = GalleryIndexView.as_view()(request)

        assert response.status_code == 200
        assert not response.context_data["featured_pets"].exists()

    @pytest.mark.django_db
    def test_template(self, rf: RequestFactory):
        """Test which template is used.

        For the index view, the 'gallery/index.html' template should be
        used.
        """
        request = rf.get(self.url)
        response = GalleryIndexView.as_view()(request)

        assert response.status_code == 200
        assert "gallery/index.html" in response.template_name
