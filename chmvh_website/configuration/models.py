from django.db import models

from solo.models import SingletonModel


class PracticeInfo(SingletonModel):
    accepting_clients = models.BooleanField(
        default=False,
        help_text=("This affects the text displayed on the 'Hours and Area' "
                   "page."),
        verbose_name='accepting new clients')
    accepting_clients_text = models.TextField(
        blank=True,
        default='',
        help_text=("This text is displayed on the 'Hours and Area' page when "
                   "'Accepting new clients' is checked."),
        verbose_name='accepting new clients message')
    address = models.TextField(
        blank=True,
        default='',
        verbose_name='practice address')
    email = models.EmailField(
        blank=True,
        default='',
        verbose_name='practice email')
    fax = models.CharField(
        blank=True,
        default='',
        max_length=17,
        verbose_name='practice fax number')
    not_accepting_clients_text = models.TextField(
        blank=True,
        default='',
        help_text=("This text is displayed on the 'Hours and Area' page when "
                   "'Accepting new clients' is <strong>not</strong> checked."),
        verbose_name='not accepting new clients message')
    phone = models.CharField(
        blank=True,
        default='',
        max_length=17,
        verbose_name='practice phone number')

    class Meta:
        verbose_name = 'practice information'

    def __str__(self):
        """Return the model's verbose name"""
        return self._meta.verbose_name.title()
