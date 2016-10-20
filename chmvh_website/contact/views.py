from django.core.urlresolvers import reverse_lazy
from django.views import generic

from contact import forms


class ContactView(generic.FormView):
    form_class = forms.ContactForm
    success_url = reverse_lazy('contact:success')
    template_name = 'contact/contact.html'


class SuccessView(generic.base.TemplateView):
    template_name = 'contact/success.html'
