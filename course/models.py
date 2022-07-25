from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from django.core.validators import MinValueValidator

from django.utils.text import slugify

class Course(models.Model):
    title = models.CharField(verbose_name=_('Course Title'), max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    cover_image = models.ImageField(verbose_name=_("Main Image"), default='default.png', upload_to='course_images')
    price = models.DecimalField(verbose_name=_("Price"), max_digits=8, decimal_places=2, default=0.0 , validators=[MinValueValidator(Decimal("0.0"))])
    rating = models.DecimalField(verbose_name=_("Ratings"), max_digits=8, decimal_places=2, default=0.0)
    raters = models.IntegerField(verbose_name=_("Number of raters"),default=0)
    students = models.IntegerField(verbose_name=_("Number of Students"), default=0)

    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def save(self, *args, **kwargs):
        print('self', dir(self))
        print('self.objects.all()', self.objects)
        self.title = str.title(self.title)
        print('self.title', self.title)
        self.slug = slugify(self.title)
        print('self.title', self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

