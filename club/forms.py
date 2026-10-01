from django import forms
from django.contrib.auth.forms import UserCreationForm

from club.models import Coach, Athlete


class AthleteForm(forms.ModelForm):
    class Meta:
        model = Athlete
        fields = "__all__"
        widgets = {
            "coaches": forms.CheckboxSelectMultiple,
            "gyms": forms.CheckboxSelectMultiple,
        }


class CoachForm(UserCreationForm):
    class Meta:
        model = Coach
        fields = "__all__"
        widgets = {
            "athletes": forms.CheckboxSelectMultiple,
            "gyms": forms.CheckboxSelectMultiple,
        }