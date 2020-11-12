from django.urls import reverse_lazy
from django.views import generic

from contact import forms


class ContactView(generic.FormView):
    form_class = forms.ContactForm
    success_url = reverse_lazy('contact:success')
    template_name = 'contact/contact.html'

    def form_valid(self, form):
        if not form.send_email():
            form.add_error(
                None, "Failed to send message. Please try again later.")

            return super(ContactView, self).form_invalid(form)

        return super(ContactView, self).form_valid(form)


class SuccessView(generic.base.TemplateView):
    template_name = 'contact/success.html'
