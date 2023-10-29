from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = "BlazeApp"
urlpatterns = [
    # Login & Logout
    path("login", views.user_login, name="user_login"),
    path("logout", login_required(views.user_logout), name="user_logout"),
    # Social Pages
    path("", login_required(views.newsfeed), name="newsfeed"),
]

handler404 = "BlazeAdministration.views.page_not_found_404"
