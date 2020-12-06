from django.conf.urls import include, url

from gallery import api_views, views


app_name = "gallery"

apiurls = [
    url(
        r"^patients/$",
        api_views.PatientListCreateView.as_view(),
        name="patient-list",
    ),
]


urlpatterns = [
    url(r"^$", views.GalleryIndexView.as_view(), name="index"),
    url(r"^api/", include((apiurls, "api"), namespace="api")),
    url(r"^memoriam/$", views.PetMemoriamView.as_view(), name="pet-memoriam"),
    url(r"^search/$", views.PatientSearchView.as_view(), name="search"),
    url(
        r"^(?P<first_letter>[a-zA-Z])/$",
        views.PetListView.as_view(),
        name="pet-list",
    ),
]
