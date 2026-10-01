from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from club.forms import UserForm, GymForm, TrainingSessionForm, UserFormUpdate
from club.models import User, Gym, TrainingSession


def index(request:HttpRequest) -> HttpResponse:

    return render(request, template_name="club/index.html")


# <---------------------------Athlete-------------------------------->

class AthleteListView(generic.ListView):
    model = User
    template_name = "club/athlete_list.html"

    def get_queryset(self):
        return User.objects.filter(role=User.Role.ATHLETE).prefetch_related("coaches")


class AthleteCreateView(LoginRequiredMixin, generic.CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("club:athletes-list")


class AthleteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserFormUpdate
    success_url = reverse_lazy("club:athletes-list")


class AthleteDetailView(generic.DetailView):
    model = User


class AthleteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("club:athletes-list")


# <---------------------------Coach-------------------------------->


class CoachListView(generic.ListView):
    model = User
    template_name = "club/coach_list.html"

    def get_queryset(self):
        return User.objects.filter(role=User.Role.COACH).prefetch_related("athletes")


class CoachCreateView(LoginRequiredMixin, generic.CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("club:coaches-list")


class CoachUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserFormUpdate
    success_url = reverse_lazy("club:coaches-list")


class CoachDetailView(generic.DetailView):
    model = User


class CoachDeleteView(generic.DeleteView):
    model = User
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
    template_name = "club/trainingsession_detail.html"

    def get_queryset(self):
        return TrainingSession.objects.select_related("coach", "gym")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_athletes"] = User.objects.filter(
            role=User.Role.ATHLETE, is_active=True
        )
        context["attended_ids"] = set(
            self.object.athletes.values_list("pk", flat=True)
        )
        return context

    def post(self, request, *args, **kwargs):
        session = self.get_object()

        if not (
            request.user.is_authenticated
            and (request.user == session.coach or request.user.is_staff)
        ):
            messages.error(request, "Нет прав отмечать посещаемость.")
            return redirect(request.path)

        ids = [int(v) for v in request.POST.getlist("attended") if v.isdigit()]
        athletes = User.objects.filter(pk__in=ids, role=User.Role.ATHLETE)

        session.athletes.set(athletes)

        messages.success(request, "Посещаемость сохранена.")
        return redirect(request.path)


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
