from django import forms
from django.core.exceptions import ValidationError
from BlazeApp.models import Post
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import FileExtensionValidator
from BlazeAdministration.customValidator import (
    validate_profilePicture_size,
)


class UserLoginForm(AuthenticationForm):
    # AuthenticationForm already has everthing necessary for login form.
    pass


class PostForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "post-content",
                "class": "col-12",
                "name": "post-content",
                "placeholder": "Write Something",
                "max_length": 1500,
                "rows": 1,
                "oninput": "autoResize(this)",
            }
        ),
        required=True,
    )

    class Meta:
        model = Post
        fields = [
            "picture",
            "content",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["picture"].widget.attrs.update(
            {
                "id": "picture-upload",
            }
        )
