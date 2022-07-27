from rest_framework import generics
from .models import Course, Lesson
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .serializers import CourseListSerializer, CourseDetailSerializer, LessonSerializer

class IsOwner(permissions.BasePermission):

    message = "You are not enrolled in this course."

    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS:
            if obj.course.instructor == request.user.profile:
                return True
            else:
                return request.user.profile in obj.course.students.all()

        return obj.course.instructor == request.user.profile


class CourseListAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user.profile)


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    lookup_field = 'slug'





class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset=Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'slug'
