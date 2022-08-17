from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination

from apps.course.models import Course
from apps.reviewers.tasks import send_course_email
from apps.users.models import Reviewer
from apps.users.serializers import CreateUserSerializer

from .permissions import ReviewerPerm
from .serializers import CreateReviewerSerializer, PendingCourseListSerializer


class PendingCoursePagination(PageNumberPagination):
    page_size = 2


class PendingCourseListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ReviewerPerm]
    serializer_class = PendingCourseListSerializer
    pagination_class = PendingCoursePagination

    def get_queryset(self):
        return Course.objects.filter(status="Pending")


class UpdatePendingCoureAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, ReviewerPerm]
    serializer_class = PendingCourseListSerializer
    pagination_class = PendingCoursePagination
    lookup_field = "slug"

    def get_queryset(self):
        return Course.objects.filter(status="Pending")

    def perform_update(self, serializer):

        if serializer.validated_data.get("status") == "Approved":
            course = Course.objects.get(slug=self.kwargs.get("slug"))
            course_title = course.title
            instructor_email = course.instructor.email

            send_course_email.delay(course_title, instructor_email)

        return super().perform_update(serializer)


class AdminCreateReviewers(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CreateReviewerSerializer
    queryset = Reviewer.objects.all()
    lookup_field = "username"
