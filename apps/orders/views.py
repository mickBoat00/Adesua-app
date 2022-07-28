from rest_framework import generics

from .models import OrderCourse

from .serializer import OrderCourseSerializer

class PayCourseAPIView(generics.ListCreateAPIView):
    queryset = OrderCourse.objects.all()
    serializer_class = OrderCourseSerializer

    def perform_create(self, serializer):
        print('seeee', serializer.validated_data)

        course = serializer.validated_data.get('course')
        person = serializer.validated_data.get('user')

        course.students.add(person)



        # course = serializer.validated_data.get('course')

        # if course.instructor != self.request.user.profile:
        #     return Response('Only course instructor can create lessons for this course.')

        serializer.save()


