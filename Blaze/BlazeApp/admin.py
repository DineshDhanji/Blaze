from django.contrib import admin

# from .models import Student, Faculty, Society
# from .models import User, Student
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ["pk", "username", "first_name", "last_name", "email"]


class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "get_username",
        "get_first_name",
        "get_last_name",
        "get_email",
        "get_major",
    ]

    def get_username(self, obj):
        return obj.user.username if obj.user else ""

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else ""

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else ""

    def get_email(self, obj):
        return obj.user.email if obj.user else ""

    def get_major(self, obj):
        return obj.major if obj.user else ""

    get_username.short_description = "username"
    get_first_name.short_description = "first name"
    get_last_name.short_description = "last name"
    get_email.short_description = "email"
    get_major.short_description = "major"


class ShareAdmin(admin.ModelAdmin):
    list_display = ["pk", "pid", "uid", "timestamp"]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ["pk", "poster", "question", "content"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["pk", "user", "object_type", "object_id", "content"]


class EventAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "poster",
        "title",
        "start_date",
        "end_date",
        "get_event_status",
        "venue",
    ]

    def get_event_status(self, obj):
        return obj.expired

    get_event_status.short_description = "Expired"


class FacultyAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "user",
        "department",
    ]


class NotificationAdmin(admin.ModelAdmin):
    list_display = ["pk", "user", "object_type", "object_id", "is_read"]


class PostAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "poster",
        "original_post",
        "get_likes_count",
        "get_saves_count",
    ]

    def get_likes_count(self, obj):
        return obj.like_count

    def get_saves_count(self, obj):
        return obj.saved_count

    get_likes_count.short_description = "Likes"
    get_saves_count.short_description = "Saves"

class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "poster",
        "title",
        "category",
    ]
class ReplyAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "aid",
        "uid",
    ]
class SocietyAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "user",
        "faculty_head",
        "president",
        "vice_president",
        "treasurer",
    ]


# Register your models here.
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Share, ShareAdmin)
admin.site.register(Society, SocietyAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(User, UserAdmin)
