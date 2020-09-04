from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def signin(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect("clients:client-list")

    context = {
        "form": form,
    }

    return render(request, "accounts/login.html", context)


@login_required
def signout(request):
    logout(request)

    return redirect("accounts:signin")
