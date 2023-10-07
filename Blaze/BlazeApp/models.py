from django.contrib.auth.models import AbstractUser, Permission, Group
from django.contrib.auth import get_user_model

from django.db import models


class Student(AbstractUser):
    Department_Choices = [("CS", "Computer Science"), ("EE", "Electrical Engineering")]
    batch = models.CharField(max_length=4)
    nuid = models.CharField(max_length=4)
    department = models.CharField(max_length=10, choices=Department_Choices)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"

    groups = models.ManyToManyField(Group, blank=True, related_name="student_set")
    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name="student_set"
    )


class Faculty(AbstractUser):
    groups = models.ManyToManyField(Group, blank=True, related_name="faculty_set")
    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name="faculty_set"
    )


class SocietyPage(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    facultyHead = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="HeadOfSociety",
    )
