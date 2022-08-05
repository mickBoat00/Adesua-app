from rest_framework import generics, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination

from apps.course.models import Course, Curriculum, Lesson

from .serializers import PendingCourseListSerializer

# Admin will create reviewers
# Reviewers will change their password
# Reviewers will update the course status after doing some background checks on the course instructor
# Course instructor will be notified about the current status of the course


class PendingCoursePagination(PageNumberPagination):
    page_size = 2


class PendingCourseListAPIView(generics.ListAPIView):
    serializer_class = PendingCourseListSerializer
    pagination_class = PendingCoursePagination

    def get_queryset(self):
        return Course.objects.filter(status="Pending")


class UpdatePendingCoureAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = PendingCourseListSerializer
    lookup_field = "slug"
    pagination_class = PendingCoursePagination

    def get_queryset(self):
        return Course.objects.filter(status="Pending")
