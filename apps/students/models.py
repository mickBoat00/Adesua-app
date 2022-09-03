from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

from .paystack import Paystack

from apps.course.models import Course
from apps.users.models import Student

import secrets

from .validators import validate_user_type


class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, related_name="enrollments", on_delete=models.CASCADE)

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

    ref = models.CharField(max_length=200)

    verified = models.BooleanField(default=False)

    course_on_free_trail = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["course", "student", "is_active"]

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = CourseEnrollment.objects.filter(ref=ref).first()
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.course.title} - {self.student.username}"


def create_paystack_transaction(sender, instance, created, **kwargs):
    if created:
        payment = Paystack()

        status = payment.make_payment(
            ref=instance.ref, 
            email=instance.student.email, 
            amount = instance.price
        )

        if status == True:
            instance.verified = True
    
        instance.save()


post_save.connect(create_paystack_transaction, sender=CourseEnrollment)
