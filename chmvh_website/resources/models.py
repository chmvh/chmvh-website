from django.db import models


class Category(models.Model):
    """A category of resources."""
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='resource category')


class Resource(models.Model):
    """A resource containing various information."""
    address = models.TextField(
        blank=True,
        verbose_name='address')
    description = models.TextField(
        blank=True,
        verbose_name='description')
    email = models.EmailField(
        blank=True,
        verbose_name='email address')
    phone = models.CharField(
        blank=True,
        max_length=50,
        verbose_name='phone number')
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='title')
    url = models.URLField(
        blank=True,
        verbose_name='website URL')

    def __str__(self):
        """Return the resource's title"""
        return self.title
