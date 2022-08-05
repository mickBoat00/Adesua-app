from rest_framework import serializers

from apps.course.models import Course, Lesson
from apps.profiles.models import Profile


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "phone_number",
            "about_me",
            "profile_photo",
            "gender",
        ]


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
    instructor = InstructorSerializer(many=False)
    curriculum = serializers.StringRelatedField(many=False)
    year = serializers.StringRelatedField(many=False)
    instructor = serializers.SerializerMethodField()
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
            "description",
            "cover_image",
            "price",
            "rating",
            "raters",
            "slug",
            "rating",
            "raters",
            "pay",
            "lessons",
        ]

    def get_instructor(self, obj):
        return obj.instructor.user.get_full_name

    def get_rating(self, obj):
        total_ratings = 0

        for rating in obj.ratings.all():
            total_ratings += rating.rating

        num_raters = obj.ratings.count()

        if num_raters <= 0:
            return 0

        return total_ratings / num_raters

    def get_raters(self, obj):
        return obj.ratings.count()
