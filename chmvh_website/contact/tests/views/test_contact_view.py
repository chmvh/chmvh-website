from unittest import mock

from django.test import RequestFactory
from django.urls import reverse

from contact.forms import ContactForm
from contact.views import ContactView


class TestContactView(object):
    """Test cases for the contact view"""

    success_url = reverse("contact:success")
    url = reverse("contact:contact")

    def test_get_initial(self, rf: RequestFactory):
        """Test the initial GET request to the view.

        The initial get request should have an empty form.
        """
        request = rf.get(self.url)
        response = ContactView.as_view()(request)

        assert response.status_code == 200

        form = response.context_data["form"]
        assert isinstance(form, ContactForm)
        assert not form.is_bound

    def test_send_email_fail(self, contact_info, rf: RequestFactory):
        """Test behavior when the email fails to send.

        If the email fails to send an error should be displayed
        informing the user that they should try again later.
        """
        request = rf.post(self.url, contact_info)

        with mock.patch(
            "contact.forms.ContactForm.send_email",
            autospec=True,
            return_value=False,
        ):
            response = ContactView.as_view()(request)

        assert response.status_code == 200

        form = response.context_data["form"]
        assert form.is_bound
        assert form.errors == {
            "__all__": ["Failed to send message. Please try again later."],
        }

    def test_submit(self, contact_info, rf: RequestFactory):
        """Test submitting a valid form.

        Submitting a valid form should send an email and redirect to
        the success url.
        """
        request = rf.post(self.url, contact_info)

        with mock.patch(
            "contact.forms.ContactForm.send_email",
            autospec=True,
            return_value=True,
        ) as mock_mail:
            response = ContactView.as_view()(request)

        assert response.status_code == 302
        assert response.url == self.success_url

        assert mock_mail.call_count == 1

    def test_submit_invalid_form(self, rf: RequestFactory):
        """Test submitting an invalid form.

        If an invalid form is submitted, the filled out form should be
        displayed with errors.
        """
        data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
        }
        request = rf.post(self.url, data)
        response = ContactView.as_view()(request)

        assert response.status_code == 200

        form = response.context_data["form"]
        assert form.is_bound
        assert form.errors == {"message": ["This field is required."]}
