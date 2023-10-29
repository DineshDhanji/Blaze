from django import forms
from django.core.exceptions import ValidationError
from BlazeApp.models import User, Student, Faculty
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class UserLoginForm(AuthenticationForm):
    pass