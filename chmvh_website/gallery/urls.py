from django.conf.urls import url

from gallery import views


urlpatterns = [
    url(r'^$', views.GalleryIndexView.as_view(), name='index'),
    url(r'^(?P<first_letter>[a-zA-Z])/$', views.PetListView.as_view(),
        name='pet-list'),
]
