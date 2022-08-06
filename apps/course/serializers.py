from rest_framework import serializers

from .models import Course, Lesson


class CourseListSerializer(serializers.ModelSerializer):
    curriculum = serializers.StringRelatedField(many=False)
    year = serializers.StringRelatedField(many=False)
    instructor = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    raters = serializers.SerializerMethodField()

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


class InstructorCourseInlineSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)


class InstructorProfileSerializer(serializers.Serializer):
    user = serializers.CharField()
    about_me = serializers.CharField()
    other_course = serializers.SerializerMethodField(read_only=True)

    def get_other_course(self, obj):
        instructor_courses = obj.instructor.all()[:4]
        return InstructorCourseInlineSerializer(instructor_courses, many=True).data


class CourseDetailSerializer(serializers.ModelSerializer):
    instructor = InstructorProfileSerializer()
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
            "instructor",
        ]
        read_only_fields = ["slug", "rating", "raters", "status", "students"]

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
    # course = serializers.PrimaryKeyRelatedField(many=False, queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = [
            # "course",
            "id",
            "title",
            "slug",
            "description",
            "video",
        ]

        read_only = ["course"]
