from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from club.forms import AthleteForm, CoachForm, GymForm, TrainingSessionForm
from club.models import Athlete, Coach, Gym, TrainingSession


def index(request:HttpRequest) -> HttpResponse:

    return render(request, template_name="club/index.html")


# <---------------------------Athlete-------------------------------->

class AthleteListView(generic.ListView):
    model = Athlete

    def get_queryset(self):
        return Athlete.objects.prefetch_related("coaches","gyms","sessions")


class AthleteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Athlete
    form_class = AthleteForm
    success_url = reverse_lazy("club:athletes-list")


class AthleteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Athlete
    form_class = AthleteForm
    success_url = reverse_lazy("club:athletes-list")


class AthleteDetailView(generic.DetailView):
    model = Athlete


class AthleteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Athlete
    success_url = reverse_lazy("club:athletes-list")


# <---------------------------Coach-------------------------------->


class CoachListView(generic.ListView):
    model = Coach


class CoachCreateView(LoginRequiredMixin, generic.CreateView):
    model = Coach
    form_class = CoachForm
    success_url = reverse_lazy("club:coaches-list")


class CoachUpdateView(LoginRequiredMixin, generic.UpdateView):
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


class GymCreateView(LoginRequiredMixin, generic.CreateView):
    model = Gym
    form_class = GymForm
    success_url = reverse_lazy("club:gyms-list")


class GymUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Gym
    form_class = GymForm
    success_url = reverse_lazy("club:gyms-list")


class GymDetailView(generic.DetailView):
    model = Gym


class GymDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Gym
    success_url = reverse_lazy("club:gyms-list")


# <---------------------------TrainingSession-------------------------------->


class TrainingSessionListView(generic.ListView):
    model = TrainingSession


class TrainingSessionDetailView(generic.DetailView):
    model = TrainingSession


class TrainingSessionCreateView(LoginRequiredMixin, generic.CreateView):
    model = TrainingSession
    form_class = TrainingSessionForm
    success_url = reverse_lazy("club:sessions-list")


class TrainingSessionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TrainingSession
    form_class = TrainingSessionForm
    success_url = reverse_lazy("club:sessions-list")


class TrainingSessionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TrainingSession
    success_url = reverse_lazy("club:sessions-list")
