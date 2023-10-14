from django.contrib.auth.models import AbstractUser, Permission, Group
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from BlazeAdministration.customValidator import (
    validate_studentBatch,
    validate_studentNUID,
    validate_studentEmail,
    validate_studentUsername,
    validate_profilePicture_size,
)


class Student(AbstractUser):
    Department_Choices = [
        ("CS", "Computer Science"),
        ("SE", "Software Engineering"),
        ("AI", "Artificial Intelligence"),
        ("CYS", "Cyber Security"),
        ("EE", "Electrical Engineering"),
    ]
    username = models.CharField(max_length=7, validators=[validate_studentUsername])
    batch = models.CharField(max_length=2, validators=[validate_studentBatch])
    nuid = models.CharField(
        unique=True, max_length=4, validators=[validate_studentNUID]
    )
    department = models.CharField(max_length=30, choices=Department_Choices)
    email = models.EmailField(unique=True, validators=[validate_studentEmail])
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
        default="profile_pics/Default_Profile_Picture.png",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            ),  # Restrict allowed file extensions
            validate_profilePicture_size,  # Set a maximum file size limit (5 MB in this example)
        ],
    )

    groups = models.ManyToManyField(Group, blank=True, related_name="student_set")
    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name="student_set"
    )


# class Faculty(AbstractUser):
#     Department_Choices = [("CS", "Computer Science"), ("EE", "Electrical Engineering")]
#     department = models.CharField(
#         max_length=30, choices=Department_Choices, blank=True, null=True
#     )

#     groups = models.ManyToManyField(Group, blank=True, related_name="faculty_set")
#     user_permissions = models.ManyToManyField(
#         Permission, blank=True, related_name="faculty_set"
#     )


# class SocietyPage(models.Model):
#     name = models.CharField(max_length=30)
#     username = models.CharField(max_length=30)
#     email = models.EmailField(max_length=254, unique=True)
#     facultyHead = models.ForeignKey(
#         Faculty,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="HeadOfSociety",
#     )
