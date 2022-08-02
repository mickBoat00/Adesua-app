from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from apps.course.models import Course, Student
from apps.profiles.models import Profile


class OrderCourse(models.Model):
    course = models.ForeignKey(Course, related_name="order", on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, related_name="profile", null=True, blank=True, on_delete=models.CASCADE)
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
        unique_together = ["course", "user"]

    def __str__(self):
        return f"{self.course.title} - {self.user.user.username}"


# def create_student_enrollment(sender, instance, created, **kwargs):
#     if created:
#         Student.objects.create(course=instance.course, profile=instance.user)

# post_save.connect(create_student_enrollment,  sender=OrderCourse)
