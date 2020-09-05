from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from clients.models import Client

from .forms import PetForm
from .models import Pet


@login_required
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


@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    context = {
        "title": "Detalhes do Pet",
        "pet": pet,
    }

    return render(request, "pets/pet_detail.html", context)


@login_required
def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    if request.method == "POST":
        pet.delete()

        messages.success(request, f"O pet {pet.name} foi deletado com sucesso!")

        return redirect(pet.owner.get_absolute_url())

    context = {
        "title": "Remover Pet",
        "pet": pet,
    }

    return render(request, "pets/pet_delete_confirm.html", context)
