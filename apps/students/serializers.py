from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.students.models import CourseEnrollment
from apps.users.models import Student
from apps.users.serializers import UserSerializer

# class CreateStudentSerializer(UserSerializer):
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     password = serializers.CharField(
#         max_length=255,
#         style={
#             "input-type": "password",
#         },
#     )

#     class Meta(UserSerializer.Meta):
#         model = Student
#         fields = ["first_name", "last_name", "username", "email", "password"]

#     def create(self, validated_data):

#         return Student.objects.create(
#             username=validated_data.get("username"),
#             first_name=validated_data.get("first_name"),
#             last_name=validated_data.get("last_name"),
#             email=validated_data.get("email"),
#             password=make_password(validated_data.get("password")),
#         )


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = [
            "id",
            "course",
            "price",
        ]
