from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from djoser.serializers import UserCreateSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    about_me = serializers.CharField(source="profile.about_me")
    gender = serializers.CharField(source="profile.gender")
    phone_number = PhoneNumberField(source="profile.phone_number")
    profile_photo = serializers.ImageField(source="profile.profile_photo")
    country = CountryField(source="profile.country")
    city = serializers.CharField(source="profile.city")
    website = serializers.CharField(source="profile.website")
    twitter = serializers.CharField(source="profile.twitter")
    youtube = serializers.CharField(source="profile.youtube")
    num_reviews = serializers.CharField(source="profile.num_reviews")
    num_students = serializers.CharField(source="profile.num_students")
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "about_me",
            "gender",
            "phone_number",
            "profile_photo",
            "country",
            "city",
            "website",
            "twitter",
            "youtube",
            "num_reviews",
            "num_students",
        ]

    def get_first_name(self, obj):
        return obj.first_name.title()

    def get_last_name(self, obj):
        return obj.last_name.title()

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        # if instance.is_superuser:
        #     representation["admin"] = True
        return representation


class CreateUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ["username", "email", "first_name", "last_name", "type", "password"]
