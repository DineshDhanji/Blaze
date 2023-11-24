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
    path("profile/129s36dp#v=k35<int:uid>313d60#c3a9pvmq5c3vjg", login_required(views.profile), name="profile"),
    path("settings/", login_required(views.settings), name="settings"),
    
    path(
        "view_post/xy9i3ao40yr6zp<int:post_id>ssd&2um[a/",
        login_required(views.view_post),
        name="view_post",
    ),
    path(
        "share_post/spv023di#r05rov2<int:post_id>sh9=shu/",
        login_required(views.share_post),
        name="share_post",
    ),
    path(
        "delete_post/",
        login_required(views.delete_post),
        name="delete_post",
    ),
    path(
        "delete_comment/",
        login_required(views.delete_comment),
        name="delete_comment",
    ),
    path(
        "create_event/",
        login_required(views.create_event),
        name="create_event",
    ),
    # API Routes
    
    # API related to like
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
    # API related to save
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
    # API related to follow
    path(
        "follow_or_unfollow/<int:user_id>/",
        login_required(api_views.follow_or_unfollow),
        name="follow_or_unfollow",
    ),
    path(
        "check_follow_or_unfollow/<int:user_id>/",
        login_required(api_views.check_follow_or_unfollow),
        name="check_follow_or_unfollow",
    ),
    
    
    # Redirecting page
    path(
        "redirecting_page/",
        login_required(views.redirecting_page),
        name="redirecting_page",
    ),
    
]

handler404 = "BlazeAdministration.views.page_not_found_404"
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
