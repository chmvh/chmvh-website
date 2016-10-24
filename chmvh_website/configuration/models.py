from django.db import models

from solo.models import SingletonModel


class PracticeInfo(SingletonModel):
    accepting_clients = models.BooleanField(
        default=False,
        help_text=("This affects the text displayed on the 'Hours and Area' "
                   "page."),
        verbose_name='accepting new clients')
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
    phone = models.CharField(
        blank=True,
        default='',
        max_length=17,
        verbose_name='practice phone number')
