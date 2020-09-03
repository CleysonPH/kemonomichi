from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def signin(request):
    authentication_form = AuthenticationForm()

    if request.method == "POST":
        authentication_form = AuthenticationForm(data=request.POST)

        if authentication_form.is_valid():
            username = authentication_form.cleaned_data.get("username")
            password = authentication_form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect("clients:client-list")
            messages.error(request, "O usuário ou a senha informada está incorreta")

    context = {
        "authentication_form": authentication_form,
    }

    return render(request, "adminlte/login.html", context)


def signout(request):
    logout(request)

    return redirect("accounts:signin")