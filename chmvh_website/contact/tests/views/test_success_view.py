from django.test import RequestFactory
from django.urls import reverse

from contact.views import SuccessView


class TestSuccessView(object):
    """Test cases for the success view"""

    url = reverse("contact:success")

    def test_get(self, rf: RequestFactory):
        """Test sending a GET request to the view.

        Sending a GET request to the view should render the success
        page.
        """
        request = rf.get(self.url)
        response = SuccessView.as_view()(request)

        assert response.status_code == 200
        assert "contact/success.html" in response.template_name
