from django.urls import path, reverse_lazy
from . import views

from .customDecorator import admin_required, anonymous_required

# from django.contrib.auth.decorators import login_required

app_name = "BlazeAdministration"

urlpatterns = [
    # Dashboard Pages
    path("", admin_required(views.dashboard), name="dashboard"),
    path(
        "add_instance/<str:instanceModel>/",
        admin_required(views.add_instance),
        name="add_instance",
    ),
    path(
        "list_instance/<str:instanceModel>/",
        admin_required(views.list_instance),
        name="list_instance",
    ),
    # Login & Logout
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
    # Page Not Found
    path("page_not_found_404/", views.page_not_found_404, name="page_not_found_404"),
]

handler404 = "BlazeAdministration.views.page_not_found_404"
