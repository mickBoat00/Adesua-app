from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import permission_classes

from apps.users.models import Student

from .models import CourseEnrollment
from .serializers import CourseEnrollmentSerializer, CreateStudentSerializer


class EnrolledStudentPermission(permissions.BasePermission):
    message = "You have to be a student to enroll in a course."

    def has_permission(self, request, view):
        if request.user.type == "STUDENT":
            return True


class StudentSignUpAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = CreateStudentSerializer


class StudentEnrollmentAPIView(generics.CreateAPIView):
    permission_classes = [EnrolledStudentPermission]
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
