from django.contrib.auth.hashers import make_password
from django.db.models import Avg
from rest_framework import serializers

from apps.course.models import Course, Lesson
from apps.course.serializers import InstructorSerializer
from apps.profiles.models import Profile
from apps.users.models import Reviewer
from apps.users.serializers import UserSerializer


class CreateReviewerSerializer(UserSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    type = serializers.CharField()
    password = serializers.CharField(
        max_length=255,
        style={
            "input-type": "password",
        },
    )

    class Meta(UserSerializer.Meta):
        model = Reviewer
        fields = ["username", "email", "first_name", "last_name", "type", "password"]

    def create(self, validated_data):
        username = validated_data.get("username")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        type = validated_data.get("type")
        email = validated_data.get("email")
        password = make_password(validated_data.get("password"))

        return Reviewer.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            type=type,
        )


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "video",
        ]


class PendingCourseListSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    curriculum = serializers.StringRelatedField(many=False)
    year = serializers.StringRelatedField(many=False)
    rating = serializers.SerializerMethodField()
    raters = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "instructor",
            "curriculum",
            "year",
            "id",
            "title",
            "slug",
            "cover_image",
            "price",
            "rating",
            "raters",
            "pay",
            "lessons",
            "status",
        ]
        read_only_fields = [
            "instructor",
            "curriculum",
            "year",
            "id",
            "title",
            "slug",
            "description",
            "cover_image",
            "price",
            "rating",
            "raters",
            "rating",
            "raters",
            "pay",
            "lessons",
        ]

    def get_rating(self, obj):
        return obj.ratings.all().aggregate(Avg("rating"))

    def get_raters(self, obj):
        return obj.ratings.count()
