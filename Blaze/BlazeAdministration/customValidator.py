from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_studentBatch(value):
    if not value.isdigit():
        raise ValidationError(("Batch must only contain numbers"))


def validate_studentNUID(value):
    if not value.isdigit():
        raise ValidationError(("NUID must only contain numbers"))


def validate_studentEmail(value):
    if not value.startswith("k"):
        raise ValidationError(("Email must start with 'k'"))
    if not value[1:7].isdigit():
        raise ValidationError(("The next 6 characters must be numbers"))
    if not value.endswith("@nu.edu.pk"):
        raise ValidationError(("Email must end with '@nu.edu.pk'"))


def validate_studentUsername(value):
    if not value.startswith("k"):
        raise ValidationError(("Email must start with 'k'"))
    if not value[1:7].isdigit():
        raise ValidationError(("Username must be in the format 'k' + batch + nuid"))


def validate_profilePicture_size(value):
    limit = 7 * 1024 * 1024  # 7 MB in bytes
    if value.size > limit:
        raise ValidationError("File size cannot exceed 7 MB.")
