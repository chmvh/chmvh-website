from django.contrib import sitemaps
from django.urls import reverse


class StaticPageSitemap(sitemaps.Sitemap):
    """Sitemap for the static pages"""
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        """Get a list of url names to add to the sitemap"""
        return (
            'contact:contact', 'homepage', 'hours-and-area', 'housecalls',
            'resources:resource-list', 'services', 'team',
        )

    def location(self, item):
        """Return the url of the specified item"""
        return reverse(item)


sitemaps = {
    'static': StaticPageSitemap,
}
