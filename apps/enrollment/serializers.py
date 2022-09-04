from rest_framework import serializers

from .models import CourseEnrollment


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = [
            "id",
            "course",
            "price",
            "is_active",
            "verified",
            "course_on_free_trail",
        ]
        read_only_fields = ["id", "is_active", "verified", "course_on_free_trail"]
