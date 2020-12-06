from django.conf.urls import url

from team import views


app_name = "team"

urlpatterns = [
    url(r"^$", views.TeamListView.as_view(), name="team"),
]
