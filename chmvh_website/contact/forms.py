import logging

from smtplib import SMTPException

from django import forms
from django.conf import settings
from django.core import mail
from django.template import loader


logger = logging.getLogger('chmvh_website.{0}'.format(__name__))


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5}))

    template = loader.get_template('contact/email/message.txt')

    def send_email(self):
        subject = '[CHMVH Website] Message from {}'.format(
            self.cleaned_data['name'])

        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
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
