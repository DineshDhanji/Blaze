from django.contrib.auth.models import AbstractUser, Permission, Group
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from BlazeAdministration.customValidator import (
    validate_studentBatch,
    validate_studentNUID,
    validate_profilePicture_size,
)


class User(AbstractUser):
    # It already have first_name, last_name, email, password
    pass


class Student(models.Model):
    Department_Choices = [
        ("CS", "Computer Science"),
        ("SE", "Software Engineering"),
        ("AI", "Artificial Intelligence"),
        ("CYS", "Cyber Security"),
        ("EE", "Electrical Engineering"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    batch = models.CharField(
        max_length=2, null=True, validators=[validate_studentBatch]
    )
    nuid = models.CharField(
        unique=True, max_length=4, null=True, validators=[validate_studentNUID]
    )
    department = models.CharField(max_length=30, choices=Department_Choices, null=True)
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
