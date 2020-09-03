from django.contrib.auth.forms import UserCreationForm

from .models import Employee


class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "birth_date",
            "email",
            "role",
        )
