from django.contrib import sitemaps
from django.urls import reverse

from gallery import models


class GallerySitemap(sitemaps.Sitemap):
    """Sitemap for the gallery"""

    changefreq = "daily"
    priority = 0.5

    def items(self):
        urls = [("gallery:index", {})]

        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if models.Patient.objects.filter(
                deceased=False, first_letter=letter
            ).exists():
                urls.append(("gallery:pet-list", {"first_letter": letter}))

        if models.Patient.objects.filter(deceased=True).exists():
            urls.append(("gallery:pet-memoriam", {}))

        return urls

    def location(self, item):
        return reverse(item[0], kwargs=item[1])


class StaticPageSitemap(sitemaps.Sitemap):
    """Sitemap for the static pages"""

    changefreq = "weekly"
    priority = 0.5

    def items(self):
        """Get a list of url names to add to the sitemap"""
        return (
            "contact:contact",
            "homepage",
            "hours-and-area",
            "housecalls",
            "resources:resource-list",
            "services",
            "team",
        )

    def location(self, item):
        """Return the url of the specified item"""
        return reverse(item)


sitemaps = {
    "gallery": GallerySitemap,
    "static": StaticPageSitemap,
}
