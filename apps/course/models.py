from decimal import Decimal

from autoslug import AutoSlugField
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.profiles.models import Profile
from apps.users.models import CourseInstructor

from .validators import validate_user_type


class TimeStampModel(models.Model):
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Curriculum(TimeStampModel):
    name = models.CharField(max_length=10, verbose_name=_("Course Curriculum"))

    class Meta:
        verbose_name_plural = "Curriculum"

    def __str__(self):
        return self.name


class Year(TimeStampModel):
    value = models.CharField(max_length=2, unique=True, verbose_name=_("School Year"))

    def __str__(self):
        return self.value


class CoursePublishedManager(models.Manager):
    def get_queryset(self):
        return super(CoursePublishedManager, self).get_queryset().filter(status="Approved", published_status=True)


class Course(TimeStampModel):

    PAY_CHOICES = [
        ("Free", "Free"),
        ("Paid", "Paid"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
    ]

    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, verbose_name=_("Course Syllables"))
    year = models.ForeignKey(Year, on_delete=models.CASCADE, verbose_name=_("Class Level"))
    instructor = models.ForeignKey(
        CourseInstructor,
        verbose_name=_("Course Instructor"),
        validators=[validate_user_type],
        related_name="courses",
        on_delete=models.CASCADE,
    )
    title = models.CharField(verbose_name=_("Course Title"), max_length=100)
    slug = AutoSlugField(populate_from="title", editable=False, unique=True, always_update=True)
    description = models.TextField()
    cover_image = models.ImageField(verbose_name=_("Main Image"), default="default.png", upload_to="course_images")
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=8,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    pay = models.CharField(
        verbose_name=_("Paid / Free"),
        max_length=4,
        choices=PAY_CHOICES,
        default="Free",
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=8,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    published_status = models.BooleanField(verbose_name=_("Published Status"), default=False)

    objects = models.Manager()
    published = CoursePublishedManager()

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ("-created_on",)

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        if self.pay == "Free":
            self.price = 0.00
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Lesson(TimeStampModel):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("Lesson Title"), max_length=100)
    slug = AutoSlugField(populate_from="title", editable=True, unique=True, always_update=True)
    description = models.TextField()
    video = models.FileField(
        verbose_name=_("Lesson Video"),
        upload_to="lesson_videos",
        validators=[FileExtensionValidator(allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"])],
    )

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        unique_together = ["course", "title"]

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        super(Lesson, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
