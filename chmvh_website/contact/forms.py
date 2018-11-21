import logging

from smtplib import SMTPException

from captcha.fields import ReCaptchaField
from django import forms
from django.conf import settings
from django.core import mail
from django.template import loader


logger = logging.getLogger('chmvh_website.{0}'.format(__name__))


class ContactForm(forms.Form):
    captcha = ReCaptchaField()
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5}))
    street_address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    zipcode = forms.CharField(required=False)

    template = loader.get_template('contact/email/message.txt')

    def clean_city(self):
        """
        If no city was provided, use a default string.
        """
        if not self.cleaned_data['city']:
            return '<No City Given>'

        return self.cleaned_data['city']

    def send_email(self):
        assert self.is_valid()

        subject = '[CHMVH Website] Message from {}'.format(
            self.cleaned_data['name'])

        address_line_2_parts = [self.cleaned_data['city'], 'North Carolina']
        if self.cleaned_data['zipcode']:
            address_line_2_parts.append(self.cleaned_data['zipcode'])

        address_line_1 = self.cleaned_data['street_address']
        address_line_2 = ', '.join(address_line_2_parts)

        address = ''
        if address_line_1:
            address = '\n'.join([address_line_1, address_line_2])

        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
            'address': address,
        }

        logger.debug("Preparing to send email")

        try:
            emails_sent = mail.send_mail(
                subject,
                self.template.render(context),
                settings.DEFAULT_FROM_EMAIL,
                ['info@chapelhillvet.com'])

            logger.info("Succesfully sent email from {0}".format(
                self.cleaned_data['email']))
        except SMTPException as e:
            emails_sent = 0

            logger.exception("Failed to send email.", exc_info=e)

        return emails_sent == 1
