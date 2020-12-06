from django.urls import reverse
from django.test import TestCase

from resources import models


class TestResourceListView(TestCase):
    url = reverse("resources:resource-list")

    def test_context(self):
        """Test the context passed to the view.

        The context should contain two lists. One for categories marked
        important, and the other for the remaining categories.
        """
        important_category = models.Category.objects.create(
            title="Important Category", important=True
        )
        normal_category = models.Category.objects.create(
            title="Normal Category"
        )

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context["important_categories"],
            ["<Category: {}>".format(important_category)],
        )
        self.assertQuerysetEqual(
            response.context["categories"],
            ["<Category: {}>".format(normal_category)],
        )
