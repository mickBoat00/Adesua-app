from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Q, Sum
from rest_framework import serializers

from apps.promotion.models import Promotion, TrialCourse
from apps.users.models import CourseInstructor
from apps.users.serializers import UserSerializer

from .models import Course, Curriculum, Lesson, Year


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = [
            "id",
            "name",
        ]


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = [
            "id",
            "value",
        ]


class CourseListSerializer(serializers.ModelSerializer):
    # curriculum = serializers.StringRelatedField(many=False)
    # year = serializers.StringRelatedField(many=False)
    curriculum = CurriculumSerializer()
    year = SchoolYearSerializer()
    instructor = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    raters = serializers.SerializerMethodField()
    promotion_price = serializers.SerializerMethodField()
    on_trail = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "curriculum",
            "year",
            "id",
            "instructor",
            "title",
            "slug",
            "cover_image",
            "rating",
            "raters",
            "pay",
            "price",
            "promotion_price",
            "on_trail",
        ]
        read_only_fields = ["slug", "rating", "raters"]

    def get_on_trail(self, obj):
        try:
            x = TrialCourse.courses_on_trail.through.objects.get(Q(trail_id__is_active=True) & Q(course_id=obj.id))

            return x.on_trail

        except ObjectDoesNotExist:
            return None

    def get_promotion_price(self, obj):

        try:
            x = Promotion.courses_on_promotion.through.objects.filter(
                Q(promotion_id__is_active=True) & Q(course_id=obj.id)
            )

            discount_amount = x.aggregate(Sum("promo_price")).get("promo_price__sum")

            if discount_amount == None:
                return None

            return obj.price - discount_amount

        except ObjectDoesNotExist:
            return None

    def get_instructor(self, obj):
        return obj.instructor.get_full_name

    def get_rating(self, obj):
        rating = obj.ratings.all().aggregate(Avg("rating")).get("rating__avg")
        return rating

    def get_raters(self, obj):
        return obj.ratings.count()


class InstructorCourseInlineSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)


class CourseDetailSerializer(serializers.ModelSerializer):
    # instructor = InstructorProfileSerializer()
    # curriculum = serializers.StringRelatedField(many=False)
    # year = serializers.StringRelatedField(many=False)
    curriculum = CurriculumSerializer()
    year = SchoolYearSerializer()
    lessons = serializers.StringRelatedField(many=True)
    rating = serializers.SerializerMethodField()
    raters = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
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
            "lessons",
            "pay",
            "published_status",
            # "instructor",
        ]
        read_only_fields = ["slug", "rating", "raters", "status", "students"]

    def get_rating(self, obj):
        return obj.ratings.all().aggregate(Avg("rating"))

    def get_raters(self, obj):
        rating = obj.ratings.all().aggregate(Avg("rating")).get("rating__avg")
        return rating

    def get_students(self, obj):
        return obj.students.count()


class CourseSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "slug",
            "cover_image",
            "price",
            "rating",
            "raters",
            "pay",
        ]
        read_only_fields = ["slug", "rating", "raters"]


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "curriculum",
            "year",
            "title",
            "description",
            "cover_image",
            "price",
            "pay",
            "published_status",
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

        read_only = ["slug"]
