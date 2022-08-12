from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.course.models import Course
from apps.profiles.models import Profile
from apps.users.models import Student


class Rating(models.Model):
    class Range(models.IntegerChoices):
        RATING_1 = 1, _("Poor")
        RATING_2 = 2, _("Fair")
        RATING_3 = 3, _("Good")
        RATING_4 = 4, _("Very Good")
        RATING_5 = 5, _("Excellent")

    rater = models.ForeignKey(
        Student,
        verbose_name=_("Enrolled Student providing the rating"),
        related_name="course_ratings",
        on_delete=models.SET_NULL,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        verbose_name=_("Course being rated"),
        related_name="ratings",
        on_delete=models.SET_NULL,
        null=True,
    )
    rating = models.IntegerField(
        verbose_name=_("Rating"),
        choices=Range.choices,
        help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent",
        default=0,
    )
    comment = models.TextField(verbose_name=_("Comment"))

    class Meta:
        unique_together = ["rater", "course"]

    def __str__(self):
        return f"{self.course} --- {self.rating} ratings"
