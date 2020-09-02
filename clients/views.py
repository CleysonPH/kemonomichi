from django.shortcuts import render, get_object_or_404

from .models import Client
from .forms import ClientForm, AddressForm


def client_create(request):
    if request.method == "POST":
        client_form = ClientForm(request.POST)
        address_form = AddressForm(request.POST)

        if client_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            client = client_form.save(commit=False)
            client.address = address
            client.save()

    client_form = ClientForm()
    address_form = AddressForm()

    context = {
        "title": "Cadastro de Clientes",
        "client_form": client_form,
        "address_form": address_form,
    }

    return render(request, "clients/client_form.html", context)


def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)

    context = {
        "title": "Detalhes do Cliente",
        "client": client,
    }

    return render(request, "clients/client_detail.html", context)