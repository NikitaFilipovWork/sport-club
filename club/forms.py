from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


from club.models import User, Gym, TrainingSession
from core import settings


DT_FORMAT = "%Y-%m-%dT%H:%M"


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "role",
            "weight",
            "coaches",
        )
        widgets = {
            "coaches": forms.CheckboxSelectMultiple,
        }


class UserFormUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "password",
            "last_name",
            "email",
            "birth_date",
            "role",
            "weight",
            "coaches",
        )
        widgets = {
            "coaches": forms.CheckboxSelectMultiple,
        }


class GymForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = "__all__"
        widgets = {
            "coaches": forms.CheckboxSelectMultiple,
        }


class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = "__all__"
        widgets = {
            "athletes": forms.CheckboxSelectMultiple,
            "starts_at": forms.DateTimeInput(
                format=DT_FORMAT,
                attrs={"type": "datetime-local", "class": "form-control"},
            ),
            "ends_at": forms.DateTimeInput(
                format=DT_FORMAT,
                attrs={"type": "datetime-local", "class": "form-control"},
            ),
        }


class AthleteModelSearchForm(forms.Form):
    last_name = forms.CharField(max_length=255, required=False)


class CoachModelSearchForm(forms.Form):
    username = forms.CharField(max_length=255, required=False)
