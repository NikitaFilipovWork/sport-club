from django.urls import path


from club.views import (
    index,
    AthleteListView,
    AthleteCreateView,
    AthleteDetailView,
    AthleteDeleteView,
    AthleteUpdateView,
    CoachListView,
    CoachCreateView,
    CoachDeleteView,
    CoachUpdateView,
    CoachDetailView,
    GymListView,
    GymCreateView,
    GymDeleteView,
    GymUpdateView,
    GymDetailView,
)

app_name = "club"

urlpatterns = [
    path("", index, name="index"),
    path("athletes/", AthleteListView.as_view(), name="athletes-list"),
    path("athletes/create/", AthleteCreateView.as_view(), name="athlete-create"),
    path("athletes/<int:pk>/detail/", AthleteDetailView.as_view(), name="athlete-detail"),
    path("athletes/<int:pk>/update/", AthleteUpdateView.as_view(), name="athlete-update"),
    path("athletes/<int:pk>/delete/", AthleteDeleteView.as_view(), name="athlete-delete"),
    path("coaches/", CoachListView.as_view(), name="coaches-list"),
    path("coaches/create/", CoachCreateView.as_view(), name="coach-create"),
    path("coaches/<int:pk>/detail/", CoachDetailView.as_view(), name="coach-detail"),
    path("coaches/<int:pk>/update/", CoachUpdateView.as_view(), name="coach-update"),
    path("coaches/<int:pk>/delete/", CoachDeleteView.as_view(), name="coach-delete"),
    path("gyms/", GymListView.as_view(), name="gyms-list"),
    path("gyms/create/", GymCreateView.as_view(), name="gym-create"),
    path("gyms/<int:pk>/detail/", GymDetailView.as_view(), name="gym-detail"),
    path("gyms/<int:pk>/update/", GymUpdateView.as_view(), name="gym-update"),
    path("gyms/<int:pk>/delete/", GymDeleteView.as_view(), name="gym-delete"),
]