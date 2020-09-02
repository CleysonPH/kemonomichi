from django.shortcuts import render, get_object_or_404, redirect

from .models import Client
from .forms import ClientForm, AddressForm


def client_create(request):
    client_form = ClientForm()
    address_form = AddressForm()

    if request.method == "POST":
        client_form = ClientForm(request.POST)
        address_form = AddressForm(request.POST)

        if client_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            client = client_form.save(commit=False)
            client.address = address
            client.save()

            return redirect(client.get_absolute_url())
    context = {
        "title": "Cadastrar Cliente",
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


def client_list(request):
    clients = Client.objects.all()

    context = {
        "title": "Lista de Clientes",
        "clients": clients,
    }

    return render(request, "clients/client_list.html", context)


def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client_form = ClientForm(instance=client)
    address_form = AddressForm(instance=client.address)

    if request.method == "POST":
        client_form = ClientForm(request.POST, instance=client)
        address_form = AddressForm(request.POST, instance=client.address)

        if client_form.is_valid() and address_form.is_valid():
            address_form.save()
            client_form.save()

            return redirect(client.get_absolute_url())
    context = {
        "title": "Editar Cliente",
        "client_form": client_form,
        "address_form": address_form,
    }

    return render(request, "clients/client_form.html", context)


def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.address.delete()
        client.delete()

        return redirect("clients:client-list")

    context = {
        "title": "Remover Cliente",
        "client": client,
    }

    return render(request, "clients/client_delete_confirm.html", context)
