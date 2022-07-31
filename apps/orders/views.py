from rest_framework import generics

from apps.course.models import Student

from .serializer import OrderCourseSerializer


class PayCourseAPIView(generics.ListCreateAPIView):
    pass
    # queryset = OrderCourse.objects.all()
    # serializer_class = OrderCourseSerializer

    # def perform_create(self, serializer):
    #     print("seeee", serializer.validated_data)

    #     course = serializer.validated_data.get("course")
    #     person = self.request.user.profile

    #     Student.objects.create(course=course, profile=person)

    #     serializer.save(user=person)
