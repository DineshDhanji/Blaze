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
    list_display = ["pk", "pid", "uid", "date"]


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty)
admin.site.register(Society)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Share, ShareAdmin)
admin.site.register(Event)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Notification)


# admin.site.register(Share)
