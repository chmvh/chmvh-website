from django.db import models


class Category(models.Model):
    """A category of resources."""
    important = models.BooleanField(
        default=False,
        help_text=('Categories marked important will be shown at the top of '
                   'the resource list'),
        verbose_name='important')
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='title')

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'categories'

    def __str__(self):
        """Return the category's title"""
        return self.title


class Resource(models.Model):
    """A resource containing various information."""
    address = models.TextField(
        blank=True,
        verbose_name='address')
    category = models.ForeignKey(
        to='Category',
        verbose_name='resource category')
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

    class Meta:
        ordering = ('title',)

    def __str__(self):
        """Return the resource's title"""
        return self.title
