from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from clients.models import Client
from .forms import PetForm


def pet_create(request, owner_pk):
    owner = get_object_or_404(Client, pk=owner_pk)
    pet_form = PetForm()

    if request.method == "POST":
        pet_form = PetForm(request.POST)

        if pet_form.is_valid():
            pet = pet_form.save(commit=False)
            pet.owner = owner
            pet.save()

            return redirect(pet.get_absolute_url())
    context = {
        "title": "Cadastrar Pet",
        "pet_form": pet_form,
    }

    return render(request, "pets/pet_form.html", context)


def pet_detail(request, pk):
    return HttpResponse("TODO")