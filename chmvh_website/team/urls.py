from django.conf.urls import url

from team import views


urlpatterns = [
    url(r'^$', views.TeamListView.as_view(), name='team'),
]
