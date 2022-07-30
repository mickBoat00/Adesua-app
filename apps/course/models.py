from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from django.core.validators import MinValueValidator, FileExtensionValidator

from autoslug import AutoSlugField

from apps.profiles.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Course Instructor"))

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class CoursePublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super(CoursePublishedManager, self).get_queryset().filter(published_status=True)
        )

class Course(models.Model):

    PAY_CHOICES = [
        ('Free', 'Free'),
        ('Paid', 'Paid'),
    ]

    categories = models.ManyToManyField(Category, verbose_name=_("Course Categories"),related_name="instructor")
    instructor = models.ForeignKey(Profile, verbose_name=_("Course Instructor"), related_name="instructor", on_delete=models.DO_NOTHING)
    title = models.CharField(verbose_name=_('Course Title'), max_length=100)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    description = models.TextField()
    cover_image = models.ImageField(verbose_name=_("Main Image"), default='default.png', upload_to='course_images')
    price = models.DecimalField(verbose_name=_("Price"), max_digits=8, decimal_places=2, default=0.0,validators=[MinValueValidator(Decimal("0.0"))])
    rating = models.DecimalField(verbose_name=_("Ratings"), max_digits=8, decimal_places=2, default=0.0)
    raters = models.IntegerField(verbose_name=_("Number of raters"),default=0)
    students = models.ManyToManyField(Profile)

    pay = models.CharField(
        verbose_name=_("Paid / Free"),
        max_length=4,
        choices=PAY_CHOICES,
        default='Free',
    )

    published_status = models.BooleanField(
        verbose_name=_("Published Status"), default=False
    )

    objects = models.Manager()
    published = CoursePublishedManager()

    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        if self.pay == 'Free':
            self.price = 0.00
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('Lesson Title'), unique=True, max_length=100)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    description = models.TextField()
    video = models.FileField(verbose_name=_("Lesson Video"), upload_to='lesson_videos',null=True, blank=True,
                    validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        super(Lesson, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


