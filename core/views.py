from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from clients.models import Client
from pets.models import Pet
from employees.models import Employee
from appointments.models import Appointment


@login_required
def dashboard(request):
    last_clients = Client.objects.all()[:5]
    last_pets = Pet.objects.all()[:5]
    last_appointments = Appointment.objects.all()[:5]

    # Get all employees registred in the last five days
    last_five_days = datetime.now() - timedelta(days=5)
    last_employees = Employee.objects.filter(date_joined__gte=last_five_days)

    num_clients = len(Client.objects.all())
    num_pets = len(Pet.objects.all())
    num_employees = len(Employee.objects.all())
    num_appointments = len(Appointment.objects.all())

    chart_data = {
        "num_dogs": len(Pet.objects.filter(specie="CA")),
        "num_cats": len(Pet.objects.filter(specie="GA")),
        "num_rabbits": len(Pet.objects.filter(specie="CO")),
    }

    context = {
        "title": "Dahsboard",
        "num_clients": num_clients,
        "num_pets": num_pets,
        "num_employees": num_employees,
        "num_appointments": num_appointments,
        "last_clients": last_clients,
        "last_pets": last_pets,
        "last_employees": last_employees,
        "last_appointments": last_appointments,
        "chart_data": chart_data,
    }

    return render(request, "core/dashboard.html", context)
