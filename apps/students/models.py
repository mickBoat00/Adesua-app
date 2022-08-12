from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.course.models import Course
from apps.users.models import Student

from .validators import validate_user_type


class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, related_name="enrollments", null=True, blank=True, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student,
        related_name="courses_enrolled",
        validators=[validate_user_type],
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=8,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(Decimal("0.0"))],
    )

    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["course", "student"]

    def __str__(self):
        return f"{self.course.title} - {self.student.username}"
