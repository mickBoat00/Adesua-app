from rest_framework import generics
from .models import Course

from .serializers import CourseSerializer


class CourseListAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
