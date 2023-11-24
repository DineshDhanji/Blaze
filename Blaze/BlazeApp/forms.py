from django import forms
from django.core.exceptions import ValidationError
from BlazeApp.models import Post, Comment, Share, Event
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


class EventForm(forms.ModelForm):
    banner = forms.ImageField(
        required=True, widget=forms.ClearableFileInput(attrs={"id": "picture-upload"})
    )
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "col efi border rounded px-2",
                "placeholder": "Enter your event title",
                "style": "height: 2.3rem;",
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "col-12 efi border rounded p-2",
                "placeholder": "Enter your event description",
                "cols": "30",
                "rows": "10",
            }
        )
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "Start Date",
                "class": "col efi border rounded px-2",
                "type": "date",
                "style": "height: 2.3rem;",
            }
        )
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder": "End Date",
                "class": "col efi border rounded px-2",
                "type": "date",
                "style": "height: 2.3rem;",
            }
        )
    )
    venue = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your event venue",
                "class": "col efi border rounded px-2",
                "style": "height: 2.3rem;",
            }
        )
    )
    time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "placeholder": "Enter your event time",
                "class": "col efi border rounded px-2",
                "style": "height: 2.3rem;",
                "type": "time",
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(
                "End date should not be less than the start date."
            )

    class Meta:
        model = Event
        fields = [
            "banner",
            "title",
            "description",
            "start_date",
            "end_date",
            "venue",
            "time",
        ]
