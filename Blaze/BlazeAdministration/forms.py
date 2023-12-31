from django import forms
from django.core.exceptions import ValidationError
from BlazeApp.models import User, Student, Faculty, Society
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class AdministrationLoginForm(AuthenticationForm):
    """
    It's just an authentication form.
    """

    pass


class StudentForm(forms.ModelForm):
    """
    All of the required fields are mentioned here.
    Eventhough, fields such as firstname, last_name, email, username, and password
    are available in the User's model. We have also included them in this form. These
    fields will be then use in User model.
    """

    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter first name",
                "autocomplete": "first-name",
                "max_length": 150,
            }
        ),
        required=True,  # Set the field as required
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter last name",
                "autocomplete": "on",
                "max_length": 150,
            }
        ),
        required=True,  # Set the field as required
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "placeholder": "kBBXXXX",
                "autocomplete": "username",
                "max_length": 7,
            }
        ),
        required=True,  # Set the field as required
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "kBBXXXX@nu.edu.pk",
                "autocomplete": "email",
                "max_length": 150,
            }
        ),
        required=True,  # Set the field as required
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password",
                "autocomplete": "on",
            }
        ),
        required=True,  # Set the field as required
    )

    """
        Keep track of all fields that are needed for the creation of Student instance.
        Meta is the way of telling form to add feilds from model in the model's form.
    """

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "batch",
            "nuid",
            "major",
        ]

    """
        I have modified the default save function of the form:
            1. First, we are getting the student instance from super save (default 
            save function, but the student is not yet saved in the database because of commit=false).
            2. Then we created a User instance from the very same data of the student form.
            3. Finally, we added the user instance in the student instance (because the user is a 
                variable in the student model) and saved it. 
    """

    def save(self, commit=True):
        student = super().save(commit=False)

        # Check if a user with the given username already exists
        existing_user = User.objects.filter(
            username=self.cleaned_data["username"]
        ).first()
        if existing_user:
            raise forms.ValidationError("A user with this username already exists.")

        # Create and associate a user with the student
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
        )
        user.set_password(self.cleaned_data["password"])
        user.save()

        student.user = user  # Associate the student with the user

        if commit:
            student.save()

        return student

    """
        When data is retrieved from the submited data, it's first clean.
        Cleaning is just checking if data is valid or not (not empty, and must follow domain).
    """

    def clean(self):
        cleaned_data = super().clean()
        batch = cleaned_data.get("batch")
        nuid = cleaned_data.get("nuid")
        email = (cleaned_data.get("email")).lower()
        username = (cleaned_data.get("username")).lower()

        expectedUsername = f"k{batch}{nuid}"
        expectedEmail = f"k{batch}{nuid}@nu.edu.pk"
        if email != expectedEmail:
            self.add_error(
                "email",
                "Email must be in the format 'k' + batch + nuid + '@nu.edu.pk'. You may have entered wrong batch/nuid",
            )

        if username != expectedUsername:
            self.add_error(
                "username",
                "Username must be in the format 'k' + batch + nuid. You may have entered wrong batch/nuid",
            )

        return cleaned_data


class FacultyForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter first name",
                "autocomplete": "first-name",
                "max_length": 150,
            }
        ),
        required=True,  # Set the field as required
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter last name",
                "autocomplete": "on",
                "max_length": 150,
            }
        ),
        required=True,  # Set the field as required
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "placeholder": "first_name.last_name",
                "autocomplete": "username",
                "max_length": 7,
            }
        ),
        required=True,  # Set the field as required
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "first_name.last_name@nu.edu.pk",
                "autocomplete": "email",
                "max_length": 150,
            }
        ),
        required=True,  # Set the field as required
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password",
                "autocomplete": "on",
            }
        ),
        required=True,  # Set the field as required
    )

    class Meta:
        model = Faculty
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "department",
        ]

    def save(self, commit=True):
        faculty = super().save(commit=False)

        # Check if a user with the given username already exists
        existing_user = User.objects.filter(
            username=self.cleaned_data["username"]
        ).first()
        if existing_user:
            raise forms.ValidationError("A user with this username already exists.")

        # Create and associate a user with the student
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
        )
        user.set_password(self.cleaned_data["password"])
        user.save()

        faculty.user = user  # Associate the student with the user

        if commit:
            faculty.save()

        return faculty

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        email = (cleaned_data.get("email")).lower()
        username = (cleaned_data.get("username")).lower()

        expectedUsername = f"{first_name.lower()}.{last_name.lower()}"
        expectedEmail = f"{first_name.lower()}.{last_name.lower()}@nu.edu.pk"
        if email != expectedEmail:
            self.add_error(
                "email",
                "Email must be in the format 'first_name' + '.' + 'last_name' + '@nu.edu.pk'. You may have entered wrong first_name/last_name.",
            )

        if username != expectedUsername:
            self.add_error(
                "username",
                "Username must be in the format 'first_name' + '.' + 'last_name'. You may have entered wrong first_name/last_name.",
            )

        return cleaned_data


class SocietyForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter first name",
                "autocomplete": "first-name",
                "max_length": 150,
            }
        ),
        required=True,  # Set the field as required
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter last name",
                "autocomplete": "on",
                "max_length": 150,
            }
        ),
        required=True,  # Set the field as required
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "placeholder": "first_name.last_name",
                "autocomplete": "username",
                "max_length": 7,
            }
        ),
        required=True,  # Set the field as required
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "first_name.last_name@nu.edu.pk",
                "autocomplete": "email",
                "max_length": 150,
            }
        ),
        required=True,  # Set the field as required
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password",
                "autocomplete": "on",
            }
        ),
        required=True,  # Set the field as required
    )

    class Meta:
        model = Society
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "faculty_head",
            "president",
            "vice_president",
            "treasurer",
        ]

    def save(self, commit=True):
        society = super().save(commit=False)

        # Check if a user with the given username already exists
        existing_user = User.objects.filter(
            username=self.cleaned_data["username"]
        ).first()
        if existing_user:
            raise forms.ValidationError("A user with this username already exists.")

        # Create and associate a user with the student
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
        )
        user.set_password(self.cleaned_data["password"])
        user.save()

        society.user = user  # Associate the student with the user

        if commit:
            society.save()

        return society

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        email = (cleaned_data.get("email")).lower()
        username = (cleaned_data.get("username")).lower()

        expectedUsername = f"{first_name.lower()}.{last_name.lower()}"
        expectedEmail = f"{first_name.lower()}{last_name.lower()}@nu.edu.pk"
        if email != expectedEmail:
            self.add_error(
                "email",
                "Email must be in the format 'first_name' + 'last_name' + '@nu.edu.pk'. You may have entered wrong first_name/last_name.",
            )

        if username != expectedUsername:
            self.add_error(
                "username",
                "Username must be in the format 'first_name' + '.' + 'last_name'. You may have entered wrong first_name/last_name.",
            )

        return cleaned_data
