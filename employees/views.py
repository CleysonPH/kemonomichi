from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Employee


@login_required
def employee_list(request):
    employees = Employee.objects.all()

    context = {
        "title": "Lista de Funcionários",
        "employees": employees,
    }

    return render(request, "employees/employee_list.html", context)
