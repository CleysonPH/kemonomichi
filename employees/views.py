from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404

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


@login_required
@user_passes_test(lambda user: user.role == 1)
def employee_detail(request, username):
    employee = get_object_or_404(Employee, username=username)
    logs = LogEntry.objects.filter(user=employee.pk)

    context = {
        "title": f"Perfil de {employee.first_name}",
        "employee": employee,
        "logs": logs,
    }

    return render(request, "employees/employee_detail.html", context)
