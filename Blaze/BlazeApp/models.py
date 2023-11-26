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
    # Internally we have different table.
    follow = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def get_followers_count(self):
        return self.followers.all().count()

    @property
    def is_student(self):
        return hasattr(self, "student")

    @property
    def is_faculty(self):
        return hasattr(self, "faculty")

    @property
    def is_society(self):
        return hasattr(self, "society")

    @property
    def get_user_type(self):
        user_type = ""
        if self.is_student:
            user_type = "student"
        elif self.is_faculty:
            user_type = "faculty"
        elif self.is_society:
            user_type = "society"
        return user_type

    @property
    def ring_color(self):
        if self.get_user_type == "student":
            current_year = timezone.now().year
            difference = current_year - int(self.student.batch)

            # Define the color ranges based on the difference
            if difference == 0:
                return "#FFBF00"  # Super Saiyan
            elif difference == 1:
                return "#E32636"  # Super Saiyan God
            elif difference == 2:
                return "#23B5D3"  # Super Saiyan Blue
            elif difference >= 3:
                return "#279AF1"  # Super Saiyan God Blue
            else:
                return "#FFFFFF"
        elif self.get_user_type == "faculty":
            # You can choose a default color or handle other cases as needed
            return "#8A2BE2"
        elif self.get_user_type == "society":
            return "#00bd9d"
        else:
            # You can choose a default color or handle other cases as needed
            return "#FFFFFF"


class Student(models.Model):
    Major_Choices = [
        ("CS", "Computer Science"),
        ("SE", "Software Engineering"),
        ("AI", "Artificial Intelligence"),
        ("CYS", "Cyber Security"),
        ("EE", "Electrical Engineering"),
    ]
    # Ring_Choices = [
    #     ("#FFBF00", "Super Saiyan"),
    #     ("#E32636", "Super Saiyan God"),
    #     ("#23B5D3", "Super Saiyan Blue"),
    #     ("#279AF1", "Super Saiyan God Blue"),
    # ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    batch = models.CharField(
        max_length=2, null=True, validators=[validate_studentBatch]
    )
    nuid = models.CharField(max_length=4, null=True, validators=[validate_studentNUID])
    major = models.CharField(max_length=30, choices=Major_Choices, null=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Faculty(models.Model):
    Department_Choices = [("CS", "Computer Science"), ("EE", "Electrical Engineering")]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="faculty", null=False, default=0
    )
    department = models.CharField(
        max_length=30, choices=Department_Choices, blank=True, null=True
    )

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"


class Society(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="society")
    faculty_head = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faculty_heads",
    )
    president = models.OneToOneField(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="presidents",
    )
    vice_president = models.OneToOneField(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vice_presidents",
    )
    treasurer = models.OneToOneField(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="treasurers",
    )

    class Meta:
        verbose_name = "Society"
        verbose_name_plural = "Societies"


class Post(models.Model):
    picture = models.ImageField(
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
    content = models.CharField(
        max_length=1500,
        help_text="Enter the content of your post (up to 1500 characters).",
    )
    timestamp = models.DateTimeField(auto_now=True, null=True)
    poster = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    original_post = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="shared_posts",
    )
    # Internally this is treated as different table
    likes = models.ManyToManyField(User, related_name="liked_post", blank=True)
    saved = models.ManyToManyField(User, related_name="saved_post", blank=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def delete(self, *args, **kwargs):
        # Delete associated comments
        Comment.objects.filter(object_type="post", object_id=self.pk).delete()

        # Delete the associated image file
        if self.picture:
            self.picture.delete()
        # Delete related Share entries
        if self.original_post:
            Share.objects.filter(
                pid=self.original_post, uid=self.poster
            ).first().delete()

        Share.objects.filter(pid=self).delete()
        # Now let the super delete handle from here
        super().delete(*args, **kwargs)

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        comment = Comment.objects.filter(object_type="post", object_id=self.pk)
        return comment.count()

    @property
    def share_count(self):
        return self.shares.count()

    @property
    def saved_count(self):
        return self.saved.count()

    def __str__(self):
        return f"Post {self.pk} by {self.poster.username}"


class Comment(models.Model):
    Object_Choices = [
        ("post", "Post"),
        ("event", "Event"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, default=0, related_name="comments"
    )
    content = models.TextField(max_length=500)
    object_type = models.CharField(
        max_length=10, choices=Object_Choices, default="Post"
    )
    timestamp = models.DateTimeField(auto_now=True)
    object_id = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def save(self, *args, **kwargs):
        # Check if the associated object exists
        try:
            # Get the ContentType for the specified category
            content_type = ContentType.objects.get(model=self.object_type)
            # Get the associated object using content_type and object_id
            associated_object = content_type.get_object_for_this_type(pk=self.object_id)

        except ContentType.DoesNotExist:
            raise ValidationError(f"Invalid content type {self.object_type}.")
        except ObjectDoesNotExist:
            raise ValidationError(
                f"Object with ID {self.object_id} does not exist in the {self.object_type} category."
            )
        super().save(*args, **kwargs)


class Share(models.Model):
    pid = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="shares")
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shares")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Share"
        verbose_name_plural = "Shares"


class Event(models.Model):
    banner = models.ImageField(
        upload_to="events/",
        null=False,
        default="events/Default_Event_Picture.png",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            validate_profilePicture_size,
        ],
        help_text="Upload an image for the event.",
    )
    title = models.CharField(max_length=200, null=False, default="No Title")
    description = models.CharField(
        max_length=1500, null=False, default="No Description"
    )
    start_date = models.DateField(null=False, default="0001-01-01")
    end_date = models.DateField(null=False, default="0001-01-01")
    poster = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="events", default=0
    )
    venue = models.CharField(max_length=50, null=False, default="No Venue")
    time = models.TimeField(null=False, default="00:00")
    timestamp = models.DateTimeField(auto_now=True, null=False)
    # Internally this is treated as different table
    likes = models.ManyToManyField(User, related_name="liked_events", blank=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def delete(self, *args, **kwargs):
        # Delete associated comments
        Comment.objects.filter(object_type="event", object_id=self.pk).delete()

        # Delete the associated image file
        if self.banner:
            self.banner.delete()

        # Now let the super delete handle from here
        super().delete(*args, **kwargs)

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        comment = Comment.objects.filter(object_type="event", object_id=self.pk)
        return comment.count()


class Question(models.Model):
    Category_Choices = [
        ("Programming", "Programming"),
        ("Academics", "Academics"),
        ("Thoughts", "Thoughts"),
        ("Social Issues", "Social Issues"),
        ("Events and Meetups", "Events and Meetups"),
        ("Personal Development", "Personal Development"),
        ("Miscellaneous", "Miscellaneous"),
    ]
    title = models.CharField(max_length=200, null=False, default="No Title")
    description = models.CharField(
        max_length=1500, null=False, default="No Description"
    )
    poster = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="questions", default=0
    )
    category = models.CharField(
        max_length=50, choices=Category_Choices, null=False, default="Miscellaneous"
    )

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Answer(models.Model):
    poster = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="answers", null=False, default=0
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        null=False,
        default=0,
    )
    content = models.CharField(
        max_length=500,
        help_text="Enter the content of your answer/reply (up to 500 characters).",
    )
    timestamp = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"


class Notification(models.Model):
    Object_Choices = [
        ("Post", "Post"),
        ("Event", "Event"),
        ("Forum", "Forum"),
    ]
    content = models.TextField(max_length=500, null=False, default="No Content")
    timestamp = models.DateTimeField(auto_now=True, null=False)
    object_type = models.CharField(
        max_length=10, choices=Object_Choices, null=False, default="Post"
    )
    object_id = models.PositiveIntegerField(null=False, default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=False,
        default=0,
    )
    is_read = models.BooleanField(null=False, default=False)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def save(self, *args, **kwargs):
        # Check if the associated object exists
        try:
            # Get the ContentType for the specified category
            content_type = ContentType.objects.get(model=self.object_type)
            # Get the associated object using content_type and object_id
            associated_object = content_type.get_object_for_this_type(pk=self.object_id)

        except ContentType.DoesNotExist:
            raise ValidationError(f"Invalid content type {self.object_type}.")
        except ObjectDoesNotExist:
            raise ValidationError(
                f"Object with ID {self.object_id} does not exist in the {self.object_type} object type."
            )
        super().save(*args, **kwargs)


class Reply(models.Model):
    aid = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="replies")
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    content = models.CharField(
        max_length=500,
        help_text="Enter the content of your answer/reply (up to 500 characters).",
    )
    timestamp = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Reply"
        verbose_name_plural = "Replies"
