from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Employee


@login_required
def employee_list(request):
    employees = Employee.objects.all()

    context = {
        "title": "Lista de Funcionários",
        "employees": employees,
    }

    return render(request, "employees/employee_list.html", context)


@login_required
def profile(request):
    employee = request.user
    logs = LogEntry.objects.filter(user=employee.pk)

    context = {
        "title": f"Perfil de {employee.first_name}",
        "employee": employee,
        "logs": logs,
    }

    return render(request, "employees/employee_detail.html", context)
