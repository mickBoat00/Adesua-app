from rest_framework import generics

from apps.users.models import Student

from .models import CourseEnrollment
from .serializers import CourseEnrollmentSerializer, CreateStudentSerializer


class StudentSignUpAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = CreateStudentSerializer


class StudentEnrollmentAPIView(generics.CreateAPIView):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer

    # def perform_create(self):
    #     pass
