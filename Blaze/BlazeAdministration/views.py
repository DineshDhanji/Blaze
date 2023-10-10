from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .customDecorator import admin_required
from django.contrib.auth.views import LoginView
from .forms import AdministrationLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def dashboard(request):
    return render(
                request,
                "BlazeAdministration/dashboard.html"
            )


def administration_login(request):
    if request.method == "POST":
        login_form = AdministrationLoginForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Attempt to sign user in
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("BlazeAdministration:dashboard")
            else:
                messages.error(request, "Invalid username and/or password.")
                return render(
                    request,
                    "account/administration_login.html",
                    {
                        "login_form": login_form,
                    },
                )
        else:
            messages.error(request, "Invalid email and/or password or submission.")
            return render(
                request, "account/administration_login.html", {"login_form": login_form}
            )
    else:
        if request.user.is_authenticated:
            return redirect("BlazeAdministration:dashboard")
        else:
            return render(
                request,
                "account/administration_login.html",
                {"login_form": AdministrationLoginForm()},
            )


def administration_logout(request):
    logout(request)
    return redirect("BlazeAdministration:administration_login")

def pageNotAccessible(request):
    return HttpResponse("<h1>Why here son?</h1>")
