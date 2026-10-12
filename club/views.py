from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from club.forms import UserForm, GymForm, TrainingSessionForm, UserFormUpdate, AthleteModelSearchForm, \
    CoachModelSearchForm, GymModelSearchForm
from club.models import User, Gym, TrainingSession


def index(request:HttpRequest) -> HttpResponse:
    total_coaches = User.objects.filter(role=User.Role.COACH).count()
    total_athletes = User.objects.filter(role=User.Role.ATHLETE).count()
    total_gyms = Gym.objects.all().count()
    context = {
        "total_coaches": total_coaches,
        "total_athletes": total_athletes,
        "total_gyms": total_gyms,
    }

    return render(request, template_name="club/index.html", context=context)


# <---------------------------Athlete-------------------------------->

class AthleteListView(generic.ListView):
    model = User
    template_name = "club/athlete_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.filter(role=User.Role.ATHLETE).prefetch_related(
            "coaches", "trainingsession_set__gym"
        )
        last_name = self.request.GET.get("last_name")

        if last_name:
            return queryset.filter(last_name__icontains=last_name)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            object_list=object_list,
            **kwargs
        )

        last_name = self.request.GET.get("last_name", "")

        context["search_form"] = AthleteModelSearchForm(
            initial={"last_name": last_name,}
        )

        return context


class AthleteCreateView(LoginRequiredMixin, generic.CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("club:athletes-list")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["can_create_athlete"] = (
                self.request.user.is_authenticated
                and (self.request.user == self.object.coach or self.request.user.is_staff)
        )

        return context

    def post(self, request, *args, **kwargs):
        session = self.get_object()

        if not (
                request.user.is_authenticated
                and (request.user == session.coach or request.user.is_staff)
        ):
            messages.error(request, "You have not enough rights(")
            return redirect(request.path)



        messages.success(request, "Saved")
        return redirect(request.path)



class AthleteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserFormUpdate
    success_url = reverse_lazy("club:athletes-list")


class AthleteDetailView(generic.DetailView):
    model = User
    template_name = "club/athlete_detail.html"
    context_object_name = "athlete"

    def get_queryset(self):
        return User.objects.filter(role=User.Role.ATHLETE).prefetch_related(
            "coaches", "trainingsession_set__gym", "trainingsession_set__coach"
        )


class AthleteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("club:athletes-list")


# <---------------------------Coach-------------------------------->


class CoachListView(generic.ListView):
    model = User
    template_name = "club/coach_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.filter(role=User.Role.COACH).prefetch_related("athletes")
        username = self.request.GET.get("username")

        if username:
            return queryset.filter(username__icontains=username)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            object_list=object_list,
            **kwargs
        )

        username = self.request.GET.get("username", "")

        context["search_form"] = CoachModelSearchForm(
            initial={"username": username,}
        )

        return context


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
    template_name = "club/coach_detail.html"
    context_object_name = "coach"

    def get_queryset(self):
        return User.objects.filter(role=User.Role.COACH).prefetch_related(
            "athletes", "gyms", "coached_sessions__gym"
        )


class CoachDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("club:coaches-list")


# <---------------------------Gym-------------------------------->


class GymListView(generic.ListView):
    model = Gym
    paginate_by = 10

    def get_queryset(self):
        queryset = Gym.objects.prefetch_related("coaches")
        address = self.request.GET.get("address")

        if address:
            return queryset.filter(address__icontains=address)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            object_list=object_list,
            **kwargs
        )

        address = self.request.GET.get("address", "")

        context["search_form"] = GymModelSearchForm(
            initial={"address": address, }
        )

        return context


class GymCreateView(LoginRequiredMixin, generic.CreateView):
    model = Gym
    form_class = GymForm
    success_url = reverse_lazy("club:gyms-list")


class GymUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Gym
    form_class = GymForm
    success_url = reverse_lazy("club:gyms-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_update_gym"] = (
            self.request.user.is_authenticated
            and (self.request.user == self.object.coach or self.request.user.is_staff)
        )

        return context


class GymDetailView(generic.DetailView):
    model = Gym
    context_object_name = "gym"

    def get_queryset(self):
        return Gym.objects.prefetch_related("coaches", "sessions__coach")


class GymDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Gym
    success_url = reverse_lazy("club:gyms-list")


# <---------------------------TrainingSession-------------------------------->


class TrainingSessionListView(generic.ListView):
    model = TrainingSession
    paginate_by = 10


class TrainingSessionDetailView(generic.DetailView):
    model = TrainingSession
    template_name = "club/trainingsession_detail.html"

    def get_queryset(self):
        return TrainingSession.objects.select_related("coach", "gym")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_mark_attendance"] = (
            self.request.user.is_authenticated
            and (self.request.user == self.object.coach or self.request.user.is_staff)
        )
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
            messages.error(request, "You have not enough rights(")
            return redirect(request.path)

        ids = [int(v) for v in request.POST.getlist("attended") if v.isdigit()]
        athletes = User.objects.filter(pk__in=ids, role=User.Role.ATHLETE)

        session.athletes.set(athletes)

        messages.success(request, "Saved")
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


class SignUpView(generic.CreateView):
    form_class = UserForm
    success_url = reverse_lazy("club:login")
    template_name = "registration/signup.html"
