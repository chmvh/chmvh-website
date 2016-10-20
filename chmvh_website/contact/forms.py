from django import forms
from django.conf import settings
from django.core import mail
from django.template import loader


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5}))

    template = loader.get_template('contact/email/message.txt')

    def send_email(self):
        subject = 'Message from {}'.format(self.cleaned_data['name'])

        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
        }

        emails_sent = mail.send_mail(
            subject,
            self.template.render(context),
            settings.DEFAULT_FROM_EMAIL,
            ['info@chapelhillvet.com'],
            fail_silently=True)

        return emails_sent == 1
