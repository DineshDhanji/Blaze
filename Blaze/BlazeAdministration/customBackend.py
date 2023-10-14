from django.contrib.auth.backends import ModelBackend
from BlazeApp.models import Student  # Import your custom user model


class StudentAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find a user with the provided username
            user = Student.objects.get(username=username)
        except Student.DoesNotExist:
            # If the user doesn't exist, return None
            return None

        # Use the user's check_password method to verify the password
        if user.check_password(password):
            return user
        else:
            return None
        
    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None
