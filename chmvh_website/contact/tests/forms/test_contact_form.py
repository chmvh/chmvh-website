from smtplib import SMTPException
from unittest import mock

from django.core import mail
from django.template import loader

from common.testing_utils import disable_logging
from contact.forms import ContactForm


class TestContactForm(object):
    """Test cases for the contact form"""

    def test_send_email(self, settings, contact_info):
        """Test sending an email from the form.

        Sending an email from the form should use the data from the
        form to construct the email.
        """
        settings.EMAIL_BACKEND = ('django.core.mail.backends.locmem.'
                                  'EmailBackend')

        template = loader.get_template('contact/email/message.txt')
        context = contact_info
        expected_subject = '[CHMVH Website] Message from {name}'.format(
            name=contact_info['name'])
        expected_body = template.render(context)
        expected_from_address = settings.DEFAULT_FROM_EMAIL
        expected_to_address = ['info@chapelhillvet.com']

        form = ContactForm(data=contact_info)

        assert form.send_email()
        assert len(mail.outbox) == 1

        message = mail.outbox[0]

        assert message.subject == expected_subject
        assert message.body == expected_body
        assert message.from_email == expected_from_address
        assert message.to == expected_to_address

    def test_send_email_fail(self, settings, contact_info):
        """Test behavior when sending an email fails.

        If the email fails to send, the method should return false.
        """
        settings.EMAIL_BACKEND = ('django.core.mail.backends.locmem.'
                                  'EmailBackend')

        form = ContactForm(data=contact_info)

        with mock.patch(
                'contact.forms.mail.send_mail',
                autospec=True,
                side_effect=SMTPException()):
            with disable_logging():
                assert not form.send_email()

        assert len(mail.outbox) == 0

    def test_validate(self, contact_info):
        """Test validating a valid form.

        If the form is valid, the validate method should return true.
        """
        form = ContactForm(data=contact_info)

        assert form.is_valid()
