import os

from django.db import models


def team_member_image_name(instance, filename):
    _, ext = os.path.splitext(filename)

    return 'team/{0}{1}'.format(instance.name, ext)


class TeamMember(models.Model):
    bio = models.TextField(
        verbose_name='biography')
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='name')
    picture = models.ImageField(
        blank=True,
        null=True,
        upload_to=team_member_image_name)

    def __str__(self):
        """Return the team member's name"""
        return self.name
