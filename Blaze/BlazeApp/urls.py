from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views
from . import api_views
from .customDecorator import normal_user_required

app_name = "BlazeApp"
urlpatterns = [
    # Login & Logout
    path("login/", views.user_login, name="user_login"),
    path("logout/", login_required(views.user_logout), name="user_logout"),
    # Settings
    path("account/followers/", login_required(views.followers), name="followers"),
    path("account/following/", login_required(views.following), name="following"),
    path("account/settings/", login_required(views.settings), name="settings"),
    path("account/remove_pp/", login_required(views.remove_pp), name="remove_pp"),
    path(
        "accounts/change_password",
        login_required(
            auth_views.PasswordChangeView.as_view(
                template_name="BlazeApp/account/password_change_form.html",
                success_url=reverse_lazy("BlazeApp:settings"),
            )
        ),
        name="password_change",
    ),
    # Social Pages
    path("", login_required(views.newsfeed), name="newsfeed"),
    path("events/", login_required(views.events), name="events"),
    path("society/", login_required(views.society), name="society"),
    path(
        "profile/129s36dpv=k35<int:uid>313d60c3a9pvmq5c3vjg",
        login_required(views.profile),
        name="profile",
    ),
    path("search/", login_required(views.search), name="search"),
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
    path(
        "delete_event/",
        login_required(views.delete_event),
        name="delete_event",
    ),
    path(
        "view_event/pqmpevna5fjc0yr6zp<int:event_id>sdhfd[m[a/",
        login_required(views.view_event),
        name="view_event",
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
    path(
        "event_like_or_unlike/<int:event_id>/",
        login_required(api_views.event_like_or_unlike),
        name="event_like_or_unlike",
    ),
    path(
        "event_check_like_or_unlike/<int:event_id>/",
        login_required(api_views.event_check_like_or_unlike),
        name="event_check_like_or_unlike",
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
    # API related to Reply
    path(
        "get_reply/<int:rid>/",
        login_required(api_views.get_reply),
        name="get_reply",
    ),
    path(
        "delete_reply/<int:rid>/",
        login_required(api_views.delete_reply),
        name="delete_reply",
    ),
    path(
        "create_reply/<int:aid>/<str:new_reply>/",
        login_required(api_views.create_reply),
        name="create_reply",
    ),
    # API related to Answer
    path(
        "get_answer/<int:aid>/",
        login_required(api_views.get_answer),
        name="get_answer",
    ),
    # API related to Notification
    path(
        "read/<int:nid>/",
        login_required(api_views.noti_read),
        name="noti_read",
    ),
    path(
        "notification_heart_beat/",
        login_required(api_views.notification_heart_beat),
        name="notification_heart_beat",
    ),
    # Forum
    path(
        "forum/",
        login_required(views.forum),
        name="forum",
    ),
    path(
        "create_thread/",
        login_required(views.create_thread),
        name="create_thread",
    ),
    path(
        "view_thread/cs2vmfps0sfd5ad<int:question_id>sdhfd[mlca73vps[a/",
        login_required(views.view_thread),
        name="view_thread",
    ),
    path(
        "delete_thread/",
        login_required(views.delete_thread),
        name="delete_thread",
    ),
    path(
        "delete_answer/",
        login_required(views.delete_answer),
        name="delete_answer",
    ),
    path(
        "forum_topics/<str:topic>/",
        login_required(views.forum_topics),
        name="forum_topics",
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
