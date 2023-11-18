from django import forms
from django.core.exceptions import ValidationError
from BlazeApp.models import Post, Comment, Share
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


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "comment",
                "class": "col-12 rounded border px-2 py-2",
                "name": "comment",
                "placeholder": "Write your thoughts ...",
                "max_length": 500,
                "rows": 1,
                "oninput": "autoResize(this)",
            }
        ),
        required=True,
    )

    class Meta:
        model = Comment
        fields = [
            "content",
        ]


class ShareForm(PostForm, forms.ModelForm):
    shared_post_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Share
        fields = [
            "shared_post_id",
        ]

    def clean_shared_post_id(self):
        shared_post_id = self.cleaned_data.get("shared_post_id")

        if shared_post_id < 0:
            raise forms.ValidationError("Invalid shared post id.")

        try:
            post = Post.objects.get(pk=shared_post_id)
        except Post.DoesNotExist:
            raise forms.ValidationError("Invalid shared post id.")

        return post

    def __init__(self, *args, **kwargs):
        shared_post_id = kwargs.pop("shared_post_id", None)
        super().__init__(*args, **kwargs)

        if shared_post_id is not None:
            self.fields["shared_post_id"].initial = shared_post_id
            self.fields["shared_post_id"].widget.attrs["readonly"] = True
