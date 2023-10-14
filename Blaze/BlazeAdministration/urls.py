from django.urls import path, reverse_lazy, re_path
from django.contrib.auth.views import LoginView
from . import views

from .customDecorator import admin_required, anonymous_required

# from django.contrib.auth.decorators import login_required

app_name = "BlazeAdministration"

urlpatterns = [
    # Dashboard Pages
    # path("", admin_required(views.dashboard), name="dashboard"),
    path("", views.dashboard, name="dashboard"),
    path(
        "add_instance/<str:instanceModel>/",
        admin_required(views.add_instance),
        name="add_instance",
    ),
    # Login & Logout
    path(
        "administration_login/",
        anonymous_required(views.administration_login),
        name="administration_login",
    ),
    # path(
    #     "administration_logout/",
    #     admin_required(views.administration_logout),
    #     name="administration_logout",
    # ),
    path(
        "administration_logout/",
        views.administration_logout,
        name="administration_logout",
    ),
    # Inaccessible
    re_path(r"^.*/", views.page_not_found_404, name="page_not_found_404"),
]
