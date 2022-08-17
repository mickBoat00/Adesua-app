from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Q, Sum
from rest_framework import serializers

from apps.promotion.models import Promotion
from apps.users.models import CourseInstructor
from apps.users.serializers import UserSerializer

from .models import Course, Lesson


class CourseListSerializer(serializers.ModelSerializer):
    curriculum = serializers.StringRelatedField(many=False)
    year = serializers.StringRelatedField(many=False)
    instructor = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    raters = serializers.SerializerMethodField()
    promotion_price = serializers.SerializerMethodField()

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
        ]
        read_only_fields = ["slug", "rating", "raters"]

    def get_promotion_price(self, obj):
        # x = obj.CoursesOnPromotion.first()
        # y = obj.courses_on_promotion.first()

        # if x and y.is_active:
        #     return x.promo_price

        try:
            x = Promotion.courses_on_promotion.through.objects.filter(
                Q(promotion_id__is_active=True) & Q(course_id=obj.id)
            )

            print("x", x)
            for a in x:
                print("a.promo_price", a.promo_price)
                print("00000000000000000000000000000000000")
            # x = Promotion.courses_on_promotion.through.objects.filter(
            #     Q(promotion_id__is_active=True) & Q(course_id=obj.id)
            # ).aggregate(Sum("promo_price"))

            # print(x)

            # return x.get("promo_price__sum")
            return 10

        except ObjectDoesNotExist:
            return None

    def get_instructor(self, obj):
        return obj.instructor.get_full_name

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


class InstructorCourseInlineSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)


class CourseDetailSerializer(serializers.ModelSerializer):
    # instructor = InstructorProfileSerializer()
    curriculum = serializers.StringRelatedField(many=False)
    year = serializers.StringRelatedField(many=False)
    lessons = serializers.StringRelatedField(many=True)
    rating = serializers.SerializerMethodField()
    raters = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

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
            "students",
            "lessons",
            "pay",
            "published_status",
            # "instructor",
        ]
        read_only_fields = ["slug", "rating", "raters", "status", "students"]

    def get_rating(self, obj):
        return obj.ratings.all().aggregate(Avg("rating"))

    def get_raters(self, obj):
        return obj.ratings.count()

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
