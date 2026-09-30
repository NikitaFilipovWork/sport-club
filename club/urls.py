from django.urls import path


from club.views import index, AthleteListView, AthleteCreateView

app_name = "club"

urlpatterns = [
    path("", index, name="index"),
    path("athletes/", AthleteListView.as_view(), name="athletes-list"),
    path("athletes/create", AthleteCreateView.as_view(), name="athletes-create"),
]