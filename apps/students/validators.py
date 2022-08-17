from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


def validate_user_type(value):
    user = User.objects.get(pk=value)

    if user.type != "STUDENT":
        raise ValidationError(
            _(f"Only students can enroll in a course"),
        )
