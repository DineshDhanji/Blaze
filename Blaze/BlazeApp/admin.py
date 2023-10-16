from django.contrib import admin

# from .models import Student, Faculty, SocietyPage
from .models import User, Student


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email"]


class StudentAdmin(admin.ModelAdmin):
    list_display = ["get_username", "get_first_name", "get_last_name", "get_email"]

    def get_username(self, obj):
        return obj.user.username if obj.user else ""

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else ""

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else ""

    def get_email(self, obj):
        return obj.user.email if obj.user else ""

    get_username.short_description = "username"
    get_first_name.short_description = "first name"
    get_last_name.short_description = "last name"
    get_email.short_description = "email"


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)

# admin.site.register(Faculty)
# admin.site.register(SocietyPage)
