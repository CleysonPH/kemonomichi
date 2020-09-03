from django import forms
from django.forms.widgets import DateInput

from .models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        exclude = ["owner"]
        widgets = {
            "birth_date": DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
        }
