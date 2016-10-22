from django.conf.urls import url

from gallery import views


urlpatterns = [
    url(r'^$', views.GalleryIndexView.as_view(), name='index'),
    url(r'^memoriam/$', views.PetMemoriamView.as_view(), name='pet-memoriam'),
    url(r'^search/$', views.PetSearchView.as_view(), name='search'),
    url(r'^(?P<first_letter>[a-zA-Z])/$', views.PetListView.as_view(),
        name='pet-list'),
]
