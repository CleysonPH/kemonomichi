from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from clients.models import Client
from pets.models import Pet
from employees.models import Employee
from appointments.models import Appointment


@login_required
def dashboard(request):
    clients = Client.objects.all()
    pets = Pet.objects.all()
    employees = Employee.objects.all()
    appointments = Appointment.objects.all()

    chart_data = {
        "num_dogs": len(Pet.objects.filter(specie="CA")),
        "num_cats": len(Pet.objects.filter(specie="GA")),
        "num_rabbits": len(Pet.objects.filter(specie="CO")),
    }

    context = {
        "title": "Dahsboard",
        "clients": clients,
        "pets": pets,
        "employees": employees,
        "appointments": appointments,
        "chart_data": chart_data,
    }

    return render(request, "core/dashboard.html", context)
