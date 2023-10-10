from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView
from . import views

from .customDecorator import admin_required, anonymous_required

# from django.contrib.auth.decorators import login_required

app_name = "BlazeAdministration"

urlpatterns = [
    path("", admin_required(views.dashboard), name="dashboard"),
    path(
        "administration_login/",
        anonymous_required(views.administration_login),
        name="administration_login",
    ),
    path(
        "administration_logout/",
        admin_required(views.administration_logout),
        name="administration_logout",
    ),
    path("page_not_accessible/", views.pageNotAccessible, name="pageNotAccessible"),
]
