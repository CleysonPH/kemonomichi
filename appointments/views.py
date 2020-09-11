from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.utils import log_addition, log_change, log_deletion
from pets.models import Pet
from .forms import AppointmentForm
from .models import Appointment


@login_required
def appointments_list(request):
    appointments = Appointment.objects.all()

    context = {
        "title": "Lista de Consultas",
        "appointments": appointments,
    }

    return render(request, "appointments/appointment_list.html", context)


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

            log_addition(request, appointment)
            messages.success(
                request,
                f"A consulta do pet {appointment.pet.name} foi criada com sucesso!",
            )

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


@login_required
@user_passes_test(lambda user: user.role in [1, 2])
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment_form = AppointmentForm(instance=appointment)

    if request.method == "POST":
        appointment_form = AppointmentForm(request.POST, instance=appointment)

        if appointment_form.is_valid():
            appointment = appointment_form.save()

            log_change(request, appointment, appointment_form, None)
            messages.success(
                request,
                f"A consulta do pet {appointment.pet.name} foi editada com sucesso!",
            )

            return redirect(appointment.get_absolute_url())
    context = {
        "title": "Editar Consulta",
        "appointment_form": appointment_form,
    }

    return render(request, "appointments/appointment_form.html", context)


@login_required
@user_passes_test(lambda user: user.role in [1, 2])
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == "POST":
        appointment.delete()

        log_deletion(request, appointment)
        messages.success(
            request,
            f"Consulta do pet {appointment.pet.name} foi removida com sucesso!",
        )

        return redirect("appointments:appointment-list")
    context = {
        "title": "Remover Consulta",
        "appointment": appointment,
    }

    return render(request, "appointments/appointments_delete_confirm.html", context)


@login_required
def appointment_send_mail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    appointment.send_mail()

    return redirect(appointment.get_absolute_url())
