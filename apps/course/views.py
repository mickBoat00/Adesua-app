from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from apps.promotion.tasks import activate_user_promotion

from .models import Course, Lesson
from .permissions import AACourseInstrutorPerm, LessonsDetailPerm
from .serializers import (
    AACourseCreateSerializer,
    AACourseDetailSerializer,
    CourseListSerializer,
    LessonSerializer,
)


class CourseModelViewset(viewsets.ModelViewSet):
    permission_classes = [AACourseInstrutorPerm]
    serializer_class = CourseListSerializer
    queryset = Course.objects.all()
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer

        elif self.action == "retrieve":
            return AACourseDetailSerializer

        return AACourseCreateSerializer


class LessonModelViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, LessonsDetailPerm]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    lookup_field = "slug"
    pagination_class = None

    def list(self, request, *args, **kwargs):
        course_slug = self.kwargs.get("courseslug")
        lessons = self.queryset.filter(course__slug=course_slug)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    def get_object(self):
        course_slug = self.kwargs.get("courseslug")
        lesson_slug = self.kwargs.get("slug")
        obj = get_object_or_404(Lesson, slug=lesson_slug, course__slug=course_slug)
        return obj

    def perform_create(self, serializer):
        course = Course.objects.get(slug=self.kwargs.get("courseslug"))
        return serializer.save(course=course)
