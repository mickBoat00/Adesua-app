from adesua.settings import AUTH_USER_MODEL
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

User = AUTH_USER_MODEL


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")
    OTHER = "Other", _("Other")


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    current_school_working = models.CharField(verbose_name=_("The school you're currently teacing"),max_length=100,)
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"), max_length=30, default="+233559875250")
    about_me = models.TextField(verbose_name=_("About me"), default="say something about yourself")
    profile_photo = models.ImageField(verbose_name=_("Profile Photo"), default="/profile_default.png")
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )
    country = models.CharField(verbose_name=_("Country"), default="Ghana", max_length=100, blank=False, null=False)
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Accra",
        blank=False,
        null=False,
    )
    website = models.URLField(verbose_name=_("My Website"), null=True, blank=True)
    twitter = models.URLField(verbose_name=_("My Twitter"), null=True, blank=True)
    youtube = models.URLField(verbose_name=_("My Youtube"), null=True, blank=True)

    num_reviews = models.IntegerField(verbose_name=_("Number of Reviews"), default=0, null=True, blank=True)
    num_students = models.IntegerField(verbose_name=_("Number of Students"), default=0, null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
