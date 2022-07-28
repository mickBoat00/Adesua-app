from rest_framework import generics
from .models import Course, Lesson
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response

from .africa_iso import iso_list

from .serializers import CourseListSerializer, CourseDetailSerializer, LessonSerializer

class IsOwner(permissions.BasePermission):

    message = "You are not allowed to perform this action."

    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS:
            if obj.course.instructor == request.user.profile:
                return True
            else:
                return request.user.profile in obj.course.students.all()

        return obj.course.instructor == request.user.profile

class aOwner(permissions.BasePermission):

    message = "You are not allowed to perform this action."

    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS:
            if request.user.is_anonymous:
                return True
            return True

        elif not request.user.is_anonymous:
            return obj.instructor == request.user.profile


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.published.all()
    serializer_class = CourseListSerializer


class CourseCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer

    def perform_create(self, serializer):
        """
        From django_countries docs, it uses ISO 3166-1 country codes
        """
        
        if self.request.user.profile.country not in iso_list(): 
            return Response('You are not African.')

        serializer.save(instructor=self.request.user.profile)


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [aOwner]
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    lookup_field = 'slug'


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')

        if course.instructor != self.request.user.profile:
            print('here??')
            return Response(
                {'error':'Only course instructor can create lessons for this course.'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        else:
            print('serializer', serializer)
            serializer.save()


class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset=Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'slug'


# class CourseEnrolledAPIView(generics.CreateAPIView):
#     queryset = OrderCourse.objects.all()
#     serializer_class = OrderCourseSerializer

#     def perform_create(self, serializer):
#         print('seeee', serializer.validated_data)

#         course = serializer.validated_data.get('course')
#         person = self.request.user.profile

#         course.students.add(person)

#         serializer.save(user=person)