from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Q, Sum
from rest_framework import serializers

from apps.promotion.models import Promotion, TrialCourse

User = get_user_model()

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


class OtherCourseSerializer(serializers.ModelSerializer):
    school_year = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "school_year",
        ]

    def get_school_year(self, obj):
        return obj.year.value


class InstructorSerializer(serializers.ModelSerializer):
    other_courses = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "other_courses",
        ]

        read_only_fields = fields

    def get_other_courses(self, obj):
        instructor_courses = obj.courses.all()[:5]
        return OtherCourseSerializer(instructor_courses, many=True).data


class CourseListSerializer(serializers.ModelSerializer):
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
            "id",
            "title",
            "curriculum",
            "year",
            "instructor",
            "slug",
            "cover_image",
            "rating",
            "raters",
            "enrollment_type",
            "price",
            "promotion_price",
            "on_trail",
        ]
        read_only_fields = fields

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


class CourseDetailSerializer(CourseListSerializer):
    instructor = InstructorSerializer()

    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields


# class CourseDetailSerializer(serializers.ModelSerializer):
#     curriculum = CurriculumSerializer()
#     year = SchoolYearSerializer()
#     instructor = InstructorSerializer()
#     rating = serializers.SerializerMethodField()
#     raters = serializers.SerializerMethodField()
#     promotion_price = serializers.SerializerMethodField()
#     on_trail = serializers.SerializerMethodField()

#     class Meta:
#         model = Course
#         fields = [
#             "curriculum",
#             "year",
#             "id",
#             "title",
#             "slug",
#             "cover_image",
#             "rating",
#             "raters",
#             "enrollment_type",
#             "price",
#             "promotion_price",
#             "on_trail",
#             "instructor",
#         ]
#         read_only_fields = fields

#     def get_on_trail(self, obj):
#         try:
#             x = TrialCourse.courses_on_trail.through.objects.get(Q(trail_id__is_active=True) & Q(course_id=obj.id))

#             return x.on_trail

#         except ObjectDoesNotExist:
#             return None

#     def get_promotion_price(self, obj):

#         try:
#             x = Promotion.courses_on_promotion.through.objects.filter(
#                 Q(promotion_id__is_active=True) & Q(course_id=obj.id)
#             )

#             discount_amount = x.aggregate(Sum("promo_price")).get("promo_price__sum")

#             if discount_amount == None:
#                 return None

#             return obj.price - discount_amount

#         except ObjectDoesNotExist:
#             return None

#     def get_instructor(self, obj):
#         return obj.instructor.get_full_name

#     def get_rating(self, obj):
#         rating = obj.ratings.all().aggregate(Avg("rating")).get("rating__avg")
#         return rating

#     def get_raters(self, obj):
#         return obj.ratings.count()


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "curriculum",
            "year",
            "id",
            "title",
            "cover_image",
            "enrollment_type",
            "price",
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

        read_only_fields = ["slug"]


class CourseSearchSerializer(serializers.ModelSerializer):

    curriculum = CurriculumSerializer()
    year = SchoolYearSerializer()
    instructor = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "year",
            "curriculum",
            "instructor",
            "status",
            "published_status",
        ]
        read_only_fields = fields

    def get_instructor(self, obj):
        return f"{obj.instructor.first_name} - {obj.instructor.last_name}"
