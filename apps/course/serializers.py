from rest_framework import serializers

from .models import Course, Lesson

"""
    Should not get all the data about the course from scratch
"""
class CourseListSerializer(serializers.ModelSerializer):
    instructor = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 
            'instructor', 
            'title', 
            'slug', 
            'description', 
            'cover_image', 
            'price', 
            'rating',  
            'raters', 
            'pay', 
        ]
        read_only_fields = ['slug','rating', 'raters']

    def get_instructor(self, obj):
        return obj.instructor.user.get_full_name


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'title', 
            'description', 
            'cover_image', 
            'price', 
            'pay', 
            'published_status', 
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = serializers.StringRelatedField(many=True)

    class Meta:
        model = Course
        fields = [
            'title', 
            'slug', 
            'description', 
            'cover_image', 
            'price', 
            'rating',  
            'raters', 
            'students',
            'lessons',
            'pay',
            'published_status',
        ]
        read_only_fields = ['slug','rating', 'raters', 'students']


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(many=False, queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = [
            'course',
            'id',
            'title',
            'description',
            'video',
        ]