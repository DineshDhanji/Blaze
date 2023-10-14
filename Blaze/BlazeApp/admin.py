from django.contrib import admin
# from .models import Student, Faculty, SocietyPage
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email", "department"]  # new


# Register your models here.
admin.site.register(Student, StudentAdmin)

# admin.site.register(Faculty)
# admin.site.register(SocietyPage)
