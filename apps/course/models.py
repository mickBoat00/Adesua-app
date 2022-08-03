from decimal import Decimal

from autoslug import AutoSlugField
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.profiles.models import Profile


class TimeStampModel(models.Model):
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Category(TimeStampModel):
    name = models.CharField(max_length=50, verbose_name=_("Course Instructor"))

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class CoursePublishedManager(models.Manager):
    def get_queryset(self):
        return super(CoursePublishedManager, self).get_queryset().filter(published_status=True)


class Course(TimeStampModel):

    PAY_CHOICES = [
        ("Free", "Free"),
        ("Paid", "Paid"),
    ]

    categories = models.ManyToManyField(Category, verbose_name=_("Course Categories"))
    instructor = models.ForeignKey(
        Profile,
        verbose_name=_("Course Instructor"),
        null=True,
        blank=True,
        related_name="instructor",
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(verbose_name=_("Course Title"), unique=True, max_length=100)
    slug = AutoSlugField(populate_from="title", editable=True, unique=True, always_update=True)
    description = models.TextField()
    cover_image = models.ImageField(verbose_name=_("Main Image"), default="default.png", upload_to="course_images")
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=8,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(Decimal("0.0"))],
    )

    pay = models.CharField(
        verbose_name=_("Paid / Free"),
        max_length=4,
        choices=PAY_CHOICES,
        default="Free",
    )

    published_status = models.BooleanField(verbose_name=_("Published Status"), default=False)

    objects = models.Manager()
    published = CoursePublishedManager()

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        if self.pay == "Free":
            self.price = 0.00
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Student(TimeStampModel):
    course = models.ForeignKey(Course, related_name="students", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course} --- {self.profile.user.get_full_name}"


class Lesson(TimeStampModel):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("Lesson Title"), max_length=100)
    slug = AutoSlugField(populate_from="title", editable=True, unique=True, always_update=True)
    description = models.TextField()
    video = models.FileField(
        verbose_name=_("Lesson Video"),
        upload_to="lesson_videos",
        null=True,
        blank=True,
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
