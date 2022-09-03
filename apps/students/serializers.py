from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.students.models import CourseEnrollment
from apps.users.models import Student
from apps.users.serializers import UserSerializer


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = ["id", "course", "price", "course_on_free_trail", "is_active"]
        read_only_fields = ["is_active","course_on_free_trail"]
