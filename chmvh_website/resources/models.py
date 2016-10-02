from django.db import models


class Category(models.Model):
    """A category of resources."""
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='resource category')
