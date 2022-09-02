from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from apps.promotion.tasks import activate_user_promotion

from .models import Course, Lesson
from .permissions import AACourseInstrutorPerm, LessonsDetailPerm
from .serializers import (
    CourseCreateSerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    LessonSerializer,
)
from rest_framework import filters

class CourseModelViewset(viewsets.ModelViewSet):
    permission_classes = [AACourseInstrutorPerm]
    serializer_class = CourseListSerializer
    queryset = Course.objects.select_related("year", "curriculum", "instructor")
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['price', 'year__value']
    filterset_fields = ['curriculum__name', 'year__value']

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer

        elif self.action == "retrieve":
            return CourseDetailSerializer

        return CourseCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(instructor=self.request.user)


class LessonModelViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, LessonsDetailPerm]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    lookup_field = "slug"
    pagination_class = None

    def get_queryset(self):
        course_slug = self.kwargs.get("courseslug")
        lessons = self.queryset.filter(course__slug=course_slug)
        return lessons

    def perform_create(self, serializer):
        course = Course.objects.get(slug=self.kwargs.get("courseslug"))
        return serializer.save(course=course)
