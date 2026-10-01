from django.urls import path


from club.views import (
    index,
    AthleteListView,
    AthleteCreateView,
    AthleteDetailView,
    AthleteDeleteView,
    AthleteUpdateView,
)

app_name = "club"

urlpatterns = [
    path("", index, name="index"),
    path("athletes/", AthleteListView.as_view(), name="athletes-list"),
    path("athletes/create", AthleteCreateView.as_view(), name="athletes-create"),
    path("athletes/<int:pk>/detail/", AthleteDetailView.as_view(), name="athlete-detail"),
    path("athletes/<int:pk>/update/", AthleteUpdateView.as_view(), name="athlete-update"),
    path("athletes/<int:pk>/delete/", AthleteDeleteView.as_view(), name="athlete-delete"),
]