from django.conf.urls import url

from resources import views


urlpatterns = [
    url(r'^$', views.ResourceListView.as_view(), name='resource-list'),
]
