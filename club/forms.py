from django import forms

from club.models import Coach, Athlete


class AthleteForm(forms.ModelForm):
    class Meta:
        model = Athlete
        fields = "__all__"
        widgets = {
            "coaches": forms.CheckboxSelectMultiple,
            "gyms": forms.CheckboxSelectMultiple,
        }