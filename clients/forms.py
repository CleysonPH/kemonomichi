from django import forms
from django.forms.widgets import DateInput

from .models import Client, Address


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ["address"]
        widgets = {
            "birth_date": DateInput(
                attrs={"type": "date"},
            ),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
