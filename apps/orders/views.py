from rest_framework import generics

from .models import OrderCourse

from .serializer import OrderCourseSerializer

class PayCourseAPIView(generics.ListCreateAPIView):
    queryset = OrderCourse.objects.all()
    serializer_class = OrderCourseSerializer

    def perform_create(self, serializer):
        print('seeee', serializer.validated_data)

        course = serializer.validated_data.get('course')
        person = self.request.user.profile

        course.students.add(person)

        serializer.save(user=person)


