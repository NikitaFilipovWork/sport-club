from django.urls import path

from club.views import index

app_name = "club"

urlpatterns = [
    path("", index, name="index")
]