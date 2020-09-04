from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from pets.models import Pet
from .forms import AppointmentForm
from .models import Appointment


@login_required
@user_passes_test(lambda user: user.role in [1, 2])
def appointment_create(request, pet_pk):
    pet = get_object_or_404(Pet, pk=pet_pk)
    appointment_form = AppointmentForm()

    if request.method == "POST":
        appointment_form = AppointmentForm(request.POST)

        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.pet = pet
            appointment.save()

            return redirect(pet.get_absolute_url())
    context = {
        "title": "Cadastrar Consulta",
        "appointment_form": appointment_form,
    }

    return render(request, "appointments/appointment_form.html", context)


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    context = {
        "title": "Detalhes da Consulta",
        "appointment": appointment,
    }

    return render(request, "appointments/appointment_detail.html", context)
