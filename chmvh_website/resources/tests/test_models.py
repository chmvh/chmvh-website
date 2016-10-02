from django.test import TestCase

from resources import models


class TestCategoryModel(TestCase):

    def test_creation(self):
        """Test creating a new category.

        The category should accept a title as a parameter.
        """
        category = models.Category.objects.create(title='New Category')

        self.assertEqual('New Category', category.title)
