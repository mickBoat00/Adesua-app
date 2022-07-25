from rest_framework import serializers

from .models import Course

"""
    Should not get all the data about the course from scratch
"""
class CourseListSerializer(serializers.ModelSerializer):

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
        ]
        read_only_fields = ['slug','rating', 'raters']

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
            'lessons'
        ]
        read_only_fields = ['slug','rating', 'raters', 'students']