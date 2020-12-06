from django.conf.urls import url

from resources import views


app_name = "resources"

urlpatterns = [
    url(r"^$", views.ResourceListView.as_view(), name="resource-list"),
]
