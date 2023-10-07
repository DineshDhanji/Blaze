from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView
from . import views

from .customDecorator import admin_required, anonymous_required

# from django.contrib.auth.decorators import login_required

app_name = "BlazeAdministration"

urlpatterns = [
    path("", admin_required(views.index), name="index"),
    path(
        "administration_login/",
        anonymous_required(
            LoginView.as_view(
                template_name="account/administration_login.html",
                success_url=reverse_lazy("BlazeAdministration:index"),
            )
        ),
        name="blaze_administration_login",
    ),
    path("page_not_accessible/", views.pageNotAccessible, name="pageNotAccessible"),
]
