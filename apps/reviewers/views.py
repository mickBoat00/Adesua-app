from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination

from apps.course.models import Course, Curriculum, Lesson
from apps.course.tasks import add
from apps.reviewers.tasks import send_course_email
from apps.users.models import User
from apps.users.serializers import CreateUserSerializer

from .serializers import PendingCourseListSerializer

# Admin will create reviewers
# Reviewers will change their password
# Reviewers will update the course status after doing some background checks on the course instructor
# Course instructor will be notified about the current status of the course


class ReviewerPerm(permissions.BasePermission):
    message = "You are not allowed because you're not a reviewer."

    def has_permission(self, request, view):

        if request.user.is_staff == True and request.user.is_superuser == False:
            return True

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff == True and request.user.is_superuser == False:
            return True


class PendingCoursePagination(PageNumberPagination):
    page_size = 2


class PendingCourseListAPIView(generics.ListAPIView):
    permission_classes = [ReviewerPerm]
    serializer_class = PendingCourseListSerializer
    pagination_class = PendingCoursePagination

    def get_queryset(self):
        return Course.objects.filter(status="Pending")


class UpdatePendingCoureAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [ReviewerPerm]
    serializer_class = PendingCourseListSerializer
    lookup_field = "slug"
    pagination_class = PendingCoursePagination

    def get_queryset(self):
        return Course.objects.filter(status="Pending")

    def perform_update(self, serializer):

        if serializer.validated_data.get("status") == "Approved":
            course = Course.objects.get(slug=self.kwargs.get("slug"))
            course_title = course.title
            instructor_email = course.instructor.user.email

            send_course_email.delay(course_title, instructor_email)

        return super().perform_update(serializer)


class AdminCreateReviewers(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CreateUserSerializer
    queryset = User.objects.filter(is_staff=True, is_superuser=False)
    lookup_field = "username"

    def perform_create(self, serializer):
        obj = serializer.save(is_staff=True)
        obj.set_password(serializer.validated_data.get("password"))
        obj.save()
