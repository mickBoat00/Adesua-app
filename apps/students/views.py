from rest_framework import generics
from rest_framework.decorators import permission_classes

from .models import CourseEnrollment
from .permissions import EnrolledStudentPermission
from .serializers import CourseEnrollmentSerializer


class StudentEnrollmentAPIView(generics.CreateAPIView):
    permission_classes = [EnrolledStudentPermission]
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
