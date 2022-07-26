from rest_framework import generics
from .models import Course, Lesson

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CourseListSerializer, CourseDetailSerializer, LessonSerializer


class CourseListAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    lookup_field = 'slug'

class CourseLessonListAPIView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Lesson.objects.filter(course__slug=self.kwargs.get('slug'))

    def perform_create(self, serializer):
        course = Course.objects.get(slug=self.kwargs.get('slug'))
        serializer.save(course=course)


class CourseLessonDetailAPIView(APIView):
    def get(self, request, course_slug, lesson_slug, format=None):
        queryset = Lesson.objects.get(course__slug=course_slug, slug=lesson_slug)
        serializer = LessonSerializer(queryset, many=False)
        return Response(serializer.data)    

    
class CourseLessonUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'slug'

    def get_object(self):
        return Lesson.objects.get(course__slug=self.kwargs.get('slug'), slug=self.kwargs.get('lesson_slug'))
