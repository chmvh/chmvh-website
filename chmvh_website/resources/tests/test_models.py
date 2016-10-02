from django.test import TestCase

from resources import models


class TestCategoryModel(TestCase):

    def test_creation(self):
        """Test creating a new category.

        The category should accept a title as a parameter.
        """
        category = models.Category.objects.create(
            title='New Category',
            important=True)

        self.assertEqual('New Category', category.title)
        self.assertTrue(category.important)

    def test_string_conversion(self):
        """Test converting a category to a string.

        Converting a category to a string should return the category's
        title.
        """
        category = models.Category(title='Test Category')

        self.assertEqual(category.title, str(category))


class TestResourceModel(TestCase):

    def test_creation(self):
        """Test creating a new resource.

        A resource should require a title, but be able to accept a
        variety of different information.
        """
        resource = models.Resource.objects.create(
            title='Resource',
            description='Test resource.',
            phone='(555) 555-5555',
            address='123 Example Drive\nNew York, NY 12345',
            url='http://example.com',
            email='test@example.com')

        self.assertEqual('Resource', resource.title)
        self.assertEqual('Test resource.', resource.description)
        self.assertEqual('(555) 555-5555', resource.phone)
        self.assertEqual(
            '123 Example Drive\nNew York, NY 12345', resource.address)
        self.assertEqual('http://example.com', resource.url)
        self.assertEqual('test@example.com', resource.email)

    def test_string_conversion(self):
        """Test converting a resource to a string.

        Converting a resource to a string should return the resource's
        title.
        """
        resource = models.Resource(title='Test Resource')

        self.assertEqual(resource.title, str(resource))
