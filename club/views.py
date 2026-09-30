from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from club.forms import AthleteForm
from club.models import Athlete


def index(request:HttpRequest) -> HttpResponse:

    return render(request, template_name="club/index.html")


class AthleteListView(generic.ListView):
    model = Athlete

    def get_queryset(self):
        return Athlete.objects.prefetch_related("coaches","gyms","sessions")


class AthleteCreateView(generic.CreateView):
    model = Athlete
    form_class = AthleteForm
    success_url = reverse_lazy("club:athletes-list")
