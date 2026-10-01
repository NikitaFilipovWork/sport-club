from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from club.forms import AthleteForm, CoachForm, GymForm
from club.models import Athlete, Coach, Gym


def index(request:HttpRequest) -> HttpResponse:

    return render(request, template_name="club/index.html")


# <---------------------------Athlete-------------------------------->

class AthleteListView(generic.ListView):
    model = Athlete

    def get_queryset(self):
        return Athlete.objects.prefetch_related("coaches","gyms","sessions")


class AthleteCreateView(generic.CreateView):
    model = Athlete
    form_class = AthleteForm
    success_url = reverse_lazy("club:athletes-list")


class AthleteUpdateView(generic.UpdateView):
    model = Athlete
    form_class = AthleteForm
    success_url = reverse_lazy("club:athletes-list")


class AthleteDetailView(generic.DetailView):
    model = Athlete


class AthleteDeleteView(generic.DeleteView):
    model = Athlete
    success_url = reverse_lazy("club:athletes-list")


# <---------------------------Coach-------------------------------->


class CoachListView(generic.ListView):
    model = Coach


class CoachCreateView(generic.CreateView):
    model = Coach
    form_class = CoachForm
    success_url = reverse_lazy("club:coaches-list")


class CoachUpdateView(generic.UpdateView):
    model = Coach
    form_class = CoachForm
    success_url = reverse_lazy("club:coaches-list")


class CoachDetailView(generic.DetailView):
    model = Coach


class CoachDeleteView(generic.DeleteView):
    model = Coach
    success_url = reverse_lazy("club:coaches-list")


# <---------------------------Gym-------------------------------->


class GymListView(generic.ListView):
    model = Gym


class GymCreateView(generic.CreateView):
    model = Gym
    form_class = GymForm
    success_url = reverse_lazy("club:gyms-list")


class GymUpdateView(generic.UpdateView):
    model = Gym
    form_class = GymForm
    success_url = reverse_lazy("club:gyms-list")


class GymDetailView(generic.DetailView):
    model = Gym


class GymDeleteView(generic.DeleteView):
    model = Gym
    success_url = reverse_lazy("club:gyms-list")


# <---------------------------TrainingSession-------------------------------->
