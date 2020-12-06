from django.conf.urls import url
from django.views.generic import TemplateView


homepage_view = TemplateView.as_view(template_name="staticpages/index.html")
hours_and_area_view = TemplateView.as_view(
    template_name="staticpages/hours-and-area.html"
)
housecalls_view = TemplateView.as_view(
    template_name="staticpages/housecalls.html"
)
services_view = TemplateView.as_view(template_name="staticpages/services.html")
team_view = TemplateView.as_view(template_name="staticpages/team.html")


urlpatterns = [
    url(r"^$", homepage_view, name="homepage"),
    url(r"^hours-and-area/$", hours_and_area_view, name="hours-and-area"),
    url(r"^housecalls/$", housecalls_view, name="housecalls"),
    url(r"^services/$", services_view, name="services"),
    url(r"^team/$", team_view, name="team"),
]
