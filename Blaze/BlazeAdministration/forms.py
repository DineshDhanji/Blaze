from django import forms
from django.core.exceptions import ValidationError
from BlazeApp.models import Student
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class AdministrationLoginForm(AuthenticationForm):
    pass


class StudentForm(UserCreationForm):
    class Meta:
        model = Student
        fields = [
            "email",
            "batch",
            "nuid",
            "department",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
    def clean(self):
        cleaned_data = super().clean()
        batch = cleaned_data.get("batch")
        nuid = cleaned_data.get("nuid")
        email = (cleaned_data.get("email")).lower()
        username = (cleaned_data.get("username")).lower()
        
        expectedUsername = f'k{batch}{nuid}'
        expectedEmail = f"k{batch}{nuid}@nu.edu.pk"
        if email != expectedEmail:
            self.add_error(
                "email", "Email must be in the format 'k' + batch + nuid + '@nu.edu.pk'. You may have entered wrong batch/nuid"
            )
        
        if username != expectedUsername:
            self.add_error(
                "username", "Username must be in the format 'k' + batch + nuid. You may have entered wrong batch/nuid"
            )

        return cleaned_data
