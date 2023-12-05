from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from django import forms
from .customDecorator import admin_required
from django.contrib.auth.views import LoginView
from .forms import AdministrationLoginForm, StudentForm, FacultyForm, SocietyForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from BlazeApp.models import Student, Faculty, Society


# Create your views here.
def dashboard(request):
    return render(request, "BlazeAdministration/dashboard.html")


def administration_login(request):
    if request.method == "POST":
        login_form = AdministrationLoginForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Attempt to sign user in
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect("BlazeAdministration:dashboard")
            else:
                messages.error(request, "Invalid username and/or password.")
                return render(
                    request,
                    "BlazeAdministration/account/administration_login.html",
                    {
                        "login_form": login_form,
                    },
                )

        else:
            messages.error(request, "Invalid email and/or password or submission.")
            return render(
                request,
                "BlazeAdministration/account/administration_login.html",
                {"login_form": login_form},
            )
    else:
        if request.user.is_authenticated:
            return redirect("BlazeAdministration:dashboard")
        else:
            return render(
                request,
                "BlazeAdministration/account/administration_login.html",
                {"login_form": AdministrationLoginForm()},
            )


def administration_logout(request):
    logout(request)
    return redirect("BlazeAdministration:administration_login")


def add_instance(request, instanceModel):
    entitiesList = ["student", "faculty", "society"]

    if instanceModel not in entitiesList:
        return page_not_found_404(request, exception=404, message="Are you lost bro?")

    if instanceModel == entitiesList[0]:
        if request.method == "POST":
            instanceForm = StudentForm(request.POST)
            if instanceForm.is_valid():
                try:
                    instanceForm.save()
                    messages.success(
                        request, "Student profile successfully created ヾ(≧▽≦*)o"
                    )
                except forms.ValidationError as e:
                    messages.error(request, "Integrity Error " + str(e))

                return render(
                    request,
                    "BlazeAdministration/add_instance.html",
                    {"instanceForm": StudentForm(), "model": instanceModel},
                )
            else:
                # print(instanceForm.errors)
                messages.error(request, "Something is not quiite right (。_。)")

                return render(
                    request,
                    "BlazeAdministration/add_instance.html",
                    {"instanceForm": instanceForm, "model": instanceModel},
                )
        else:
            return render(
                request,
                "BlazeAdministration/add_instance.html",
                {"instanceForm": StudentForm(), "model": instanceModel},
            )
    elif instanceModel == entitiesList[1]:
        if request.method == "POST":
            instanceForm = FacultyForm(request.POST)
            if instanceForm.is_valid():
                try:
                    instanceForm.save()
                    messages.success(
                        request, "Faculty profile successfully created ヾ(≧▽≦*)o"
                    )
                except forms.ValidationError as e:
                    messages.error(request, "Integrity Error " + str(e))

                return render(
                    request,
                    "BlazeAdministration/add_instance.html",
                    {"instanceForm": FacultyForm(), "model": instanceModel},
                )
            else:
                messages.error(request, "Something is not quiite right (。_。)")

                return render(
                    request,
                    "BlazeAdministration/add_instance.html",
                    {"instanceForm": instanceForm, "model": instanceModel},
                )
        else:
            return render(
                request,
                "BlazeAdministration/add_instance.html",
                {"instanceForm": FacultyForm(), "model": instanceModel},
            )
    elif instanceModel == entitiesList[2]:
        if request.method == "POST":
            instanceForm = SocietyForm(request.POST)
            if instanceForm.is_valid():
                try:
                    instanceForm.save()
                    messages.success(
                        request, "Society profile successfully created ヾ(≧▽≦*)o"
                    )
                except forms.ValidationError as e:
                    messages.error(request, "Integrity Error " + str(e))

                return render(
                    request,
                    "BlazeAdministration/add_instance.html",
                    {"instanceForm": SocietyForm(), "model": instanceModel},
                )
            else:
                messages.error(request, "Something is not quiite right (。_。)")

                return render(
                    request,
                    "BlazeAdministration/add_instance.html",
                    {"instanceForm": instanceForm, "model": instanceModel},
                )
        else:
            return render(
                request,
                "BlazeAdministration/add_instance.html",
                {"instanceForm": SocietyForm(), "model": instanceModel},
            )
    else:
        return page_not_found_404(request, exception=404, message="Are you lost bro?")


def list_instance(request, instanceModel):
    entitiesList = ["student", "faculty", "society"]

    if instanceModel not in entitiesList:
        return page_not_found_404(request, exception=404, message="Are you lost bro?")

    if instanceModel == entitiesList[0]:
        dataset = Student.objects.all()
    elif instanceModel == entitiesList[1]:
        dataset = Faculty.objects.all()
    else:
        dataset = Society.objects.all()

    return render(
        request,
        "BlazeAdministration/list_instance.html",
        {"model": instanceModel, "dataset": dataset},
    )


def page_not_found_404(request, exception, message=None):
    return render(
        request,
        "BlazeAdministration/page_not_found_404.html",
        {"message": message},
        status=404,
    )
