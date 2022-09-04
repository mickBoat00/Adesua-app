from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def validate_user_type(value):
    user = User.objects.get(pk=value)

    if user.type != "INSTRUCTOR":
        raise ValidationError(
            _(f"Only instructors can create courses"),
        )
