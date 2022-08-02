from rest_framework import serializers

from .models import Category, Course, Lesson

"""
    Should not get all the data about the course from scratch
"""


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# class CourseListSerializer(serializers.ModelSerializer):
#     instructor = serializers.SerializerMethodField()

#     class Meta:
#         model = Course
#         fields = [
#             'id',
#             'instructor',
#             'title',
#             'slug',
#             'description',
#             'cover_image',
#             'price',
#             'rating',
#             'raters',
#             'pay',
#         ]
#         read_only_fields = ['slug','rating', 'raters']

#     def get_instructor(self, obj):
#         return obj.instructor.user.get_full_name


class CourseListSerializer(serializers.ModelSerializer):
    instructor = serializers.SerializerMethodField()

    rating = serializers.SerializerMethodField()
    raters = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "instructor",
            "title",
            "slug",
            "description",
            "cover_image",
            "price",
            "rating",
            "raters",
            "pay",
        ]
        read_only_fields = ["slug", "rating", "raters"]

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
            "title",
            "description",
            "cover_image",
            "price",
            "pay",
            "published_status",
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = serializers.StringRelatedField(many=True)
    rating = serializers.SerializerMethodField()
    raters = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "categories",
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
        ]
        read_only_fields = ["slug", "rating", "raters", "students"]

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

    def get_students(self, obj):
        return obj.students.count()


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(many=False, queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = [
            "course",
            "id",
            "title",
            "slug",
            "description",
            "video",
        ]
