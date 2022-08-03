from rest_framework import generics, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from .african_country_list import african_countries
from .models import Course, Lesson
from .permissions import (
    CourseInstrutorPerm,
    CreateLessonPerm,
    LessonsDetailPerm,
    SingleLessonPerm,
)
from .serializers import (
    CourseCreateSerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    LessonSerializer,
)


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.published.all()
    serializer_class = CourseListSerializer


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [CourseInstrutorPerm]
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    lookup_field = "slug"


class CourseCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer

    def perform_create(self, serializer):

        if self.request.user.profile.country not in african_countries():
            """
            Research how to output this message instead
            """
            print("You are not allowed to create a ccourse")
            # return Response({"error": "You are not African."}, status=status.HTTP_403_FORBIDDEN)
            return

        serializer.save(instructor=self.request.user.profile)


class CourseLessonsAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, LessonsDetailPerm]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return super().get_queryset().filter(course__slug=self.kwargs.get("slug"))


class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, SingleLessonPerm]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = "slug"


class LessonCreateAPIView(generics.CreateAPIView):
    """
    A little bug in permissions.
    Can any course instrutor create lesson for it
    """

    permission_classes = [CreateLessonPerm]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    """
    Lesson model should have unique together between all fields
    """
