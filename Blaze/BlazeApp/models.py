from django.contrib.auth.models import AbstractUser, Permission, Group
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.shortcuts import get_object_or_404

from BlazeAdministration.customValidator import (
    validate_studentBatch,
    validate_studentNUID,
    validate_profilePicture_size,
)


class User(AbstractUser):
    # It already have first_name, last_name, email, password
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
        default="profile_pics/Default_Profile_Picture.png",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            ),  # Restrict allowed file extensions
            validate_profilePicture_size,  # Set a maximum file size limit (7 MB in this example)
        ],
    )


class Student(models.Model):
    Major_Choices = [
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
    nuid = models.CharField(max_length=4, null=True, validators=[validate_studentNUID])
    major = models.CharField(max_length=30, choices=Major_Choices, null=True)


class Faculty(models.Model):
    Department_Choices = [("CS", "Computer Science"), ("EE", "Electrical Engineering")]
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="faculty")
    department = models.CharField(
        max_length=30, choices=Department_Choices, blank=True, null=True
    )


class Society(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="society")
    faculty_head = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faculty_head",
    )
    president = models.OneToOneField(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="president",
    )
    vice_president = models.OneToOneField(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vice_president",
    )
    treasurer = models.OneToOneField(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="treasurer",
    )


class Post(models.Model):
    post_picture = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            ),  # Restrict allowed file extensions
            validate_profilePicture_size,  # Set a maximum file size limit (7 MB in this example)
        ],
        help_text="Upload an image for the post (optional).",
    )
    post_content = models.CharField(
        max_length=1500,
        help_text="Enter the content of your post (up to 1500 characters).",
    )
    date = models.DateTimeField(auto_now=True, null=True)
    poster = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="post",
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    # def __str__(self):
    #     return f"Post {self.pk} by {self.poster.username} on {self.date}"


class Comment(models.Model):
    Category_Choices = [
        ("post", "Post"),
        ("Forum", "Forum"),
        ("Event", "Event"),
    ]
    content = models.TextField(max_length=500)
    category = models.CharField(max_length=10, choices=Category_Choices)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    object_id = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        # Check if the associated object exists
        try:
            # Get the ContentType for the specified category
            content_type = ContentType.objects.get(model=self.category)
            # Get the associated object using content_type and object_id
            associated_object = content_type.get_object_for_this_type(pk=self.object_id)

        except ContentType.DoesNotExist:
            raise ValidationError(f"Invalid content type {self.category}.")
        except ObjectDoesNotExist:
            raise ValidationError(
                f"Object with ID {self.object_id} does not exist in the {self.category} category."
            )
        super().save(*args, **kwargs)
