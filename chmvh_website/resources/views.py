from django.views import generic

from resources import models


class ResourceListView(generic.base.TemplateView):
    """View for listing resources"""
    queryset = models.Category.objects.all()
    template_name = 'resources/resource-list.html'

    def get_context_data(self):
        context = super(ResourceListView, self).get_context_data()

        important_categories = self.queryset.filter(important=True)
        context['important_categories'] = important_categories

        normal_categories = self.queryset.filter(important=False)
        context['categories'] = normal_categories

        return context
