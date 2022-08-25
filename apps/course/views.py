import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from apps.promotion.tasks import activate_user_promotion
from apps.users.models import CourseInstructor

from .models import Course, Curriculum, Lesson
from .permissions import (
    CourseInstructorPerm,
    CourseInstrutorPerm,
    LessonsDetailPerm,
    SingleLessonPerm,
)
from .serializers import (
    CourseCreateSerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    LessonSerializer,
)


class CourseFilter(django_filters.FilterSet):
    curriculum__name = django_filters.CharFilter(lookup_expr="iexact")
    year__value = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Course
        fields = ["curriculum__name", "year__value"]


class CourseListAPIView(generics.ListAPIView):
    # queryset = Course.published.all()
    serializer_class = CourseListSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = CourseFilter

    def get_queryset(self):
        return Course.published.select_related("year", "curriculum", "instructor")


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [CourseInstrutorPerm]
    # queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Course.published.select_related("year", "curriculum", "instructor")


class CourseCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, CourseInstructorPerm]
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class CourseLessonsAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, LessonsDetailPerm]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return super().get_queryset().filter(course__slug=self.kwargs.get("slug"))

    def perform_create(self, serializer):

        course = Course.objects.get(slug=self.kwargs.get("slug"))

        serializer.save(course=course)


class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, SingleLessonPerm]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = "slug"
