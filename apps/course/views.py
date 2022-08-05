import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from .african_country_list import african_countries
from .models import Course, Curriculum, Lesson
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


class CourseFilter(django_filters.FilterSet):
    curriculum__name = django_filters.CharFilter(lookup_expr="iexact")
    year__value = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Course
        fields = ["curriculum__name", "year__value"]


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.published.all()
    serializer_class = CourseListSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = CourseFilter


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
        serializer.save(instructor=self.request.user.profile)

    # def create(self, request, *args, **kwargs):

    #     if request.user.profile.country not in african_countries():
    #         return Response({"error": "Sorry you are not an african"}, status=status.HTTP_403_FORBIDDEN)

    #     serializer = self.get_serializer(data=request.data)

    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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


# class LessonCreateAPIView(generics.CreateAPIView):
#     """
#     A little bug in permissions.
#     Can any course instrutor create lesson for it
#     """

#     permission_classes = [CreateLessonPerm]
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer


#     """
#     Lesson model should have unique together between all fields
#     """
