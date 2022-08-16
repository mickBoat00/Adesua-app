from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.course.models import Course

User = get_user_model()


class PromoType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    name = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=20)


class Promotion(models.Model):
    created_by = models.ForeignKey(User, related_name="promotions", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    promo_percentage = models.IntegerField(
        verbose_name=_("percentage reduction for promotion %"),
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        null=True,
        blank=True,
    )
    promo_amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=False)
    is_schedule = models.BooleanField(default=False)
    promo_start = models.DateField()
    promo_end = models.DateField()

    courses_on_promotion = models.ManyToManyField(
        Course,
        related_name="courses_on_promotion",
        through="CoursesOnPromotion",
    )

    promo_type = models.ForeignKey(
        PromoType,
        related_name="promotype",
        on_delete=models.PROTECT,
    )

    coupon = models.ForeignKey(
        Coupon,
        related_name="coupon",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def clean(self):
        if self.promo_start > self.promo_end:
            raise ValidationError(_("End data before the start date"))

        if self.promo_percentage >= 1 and self.promo_amount >= 0.01:
            raise ValidationError(_("You must select promotion percentage or amount not both"))

    def __str__(self):
        return self.name


class CoursesOnPromotion(models.Model):
    course_id = models.ForeignKey(
        Course,
        related_name="CoursesOnPromotion",
        on_delete=models.PROTECT,
    )
    promotion_id = models.ForeignKey(
        Promotion,
        related_name="promotion",
        on_delete=models.CASCADE,
    )
    promo_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )
    price_override = models.BooleanField(
        default=False,
    )

    class Meta:
        unique_together = (("course_id", "promotion_id"),)
