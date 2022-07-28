from rest_framework import serializers

from django_countries.serializer_fields import CountryField

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    country = CountryField(name_only=True)

    class Meta:
        model = Profile 
        fields = [
            'username',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'id',
            'phone_number',
            'profile_photo',
            'about_me',
            'gender',
            'country',
            'city',
            'website',
            'twitter',
            'youtube',
            'num_reviews',
            'num_students',
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"



class InstructorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    full_name = serializers.SerializerMethodField(read_only=True)
    country = CountryField(name_only=True)

    class Meta:
        model = Profile 
        fields = [
            'first_name',
            'last_name',
            'full_name',
            'profile_photo',
            'about_me',
            'country',
            'city',
            'website',
            'twitter',
            'youtube',
            'num_reviews',
            'num_students',
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"




class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            'phone_number',
            'profile_photo',
            'about_me',
            'gender',
            'country',
            'city',
            'website',
            'twitter',
            'youtube',
        ]
