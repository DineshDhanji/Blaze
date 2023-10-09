from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class AdministrationLoginForm(AuthenticationForm):
    # username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
    # password = forms.CharField(
    #     label=_("Password"),
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    # )
    
    pass
    # username = forms.CharField(
    #     widget=forms.CharField(
    #         attrs={
    #             # "class": "col-10",
    #             # "placeholder": "Enter your email",
    #             # "id": "id_email",
    #             # "autocomplete": "email",
    #         }
    #     ),
    #     max_length=50,
    #     required=True,
    # )
    # password = forms.CharField(
    #     widget=forms.PasswordInput(
    #         # attrs={"class": "password-input", "placeholder": "Enter your password"},
    #     ),
    #     max_length=50,
    #     required=True,
    # )