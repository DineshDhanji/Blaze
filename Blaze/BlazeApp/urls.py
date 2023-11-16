from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from . import api_views
from .customDecorator import normal_user_required
from django.conf import settings
from django.conf.urls.static import static

app_name = "BlazeApp"
urlpatterns = [
    # Login & Logout
    path("login/", views.user_login, name="user_login"),
    path("logout/", login_required(views.user_logout), name="user_logout"),
    # Social Pages
    path("", login_required(views.newsfeed), name="newsfeed"),
    path("events/", login_required(views.events), name="events"),
    path("society/", login_required(views.society), name="society"),
    path("profile/", login_required(views.profile), name="profile"),
    path("settings/", login_required(views.settings), name="settings"),
    
    path(
        "delete_post/",
        login_required(views.delete_post),
        name="delete_post",
    ),
    # API Routes
    
    # API related to LIKE
    path(
        "like_or_unlike/<int:post_id>/",
        login_required(api_views.like_or_unlike),
        name="like_or_unlike",
    ),
    path(
        "check_like_or_unlike/<int:post_id>/",
        login_required(api_views.check_like_or_unlike),
        name="check_like_or_unlike",
    ),
    # API related to SAVED
    path(
        "save_or_unsave/<int:post_id>/",
        login_required(api_views.save_or_unsave),
        name="save_or_unsave",
    ),
    path(
        "check_save_or_unsave/<int:post_id>/",
        login_required(api_views.check_save_or_unsave),
        name="check_save_or_unsave",
    ),
]

handler404 = "BlazeAdministration.views.page_not_found_404"
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
