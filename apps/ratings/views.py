from rest_framework import generics ,status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import permission_classes

from .models import Rating
from .serializers import RatingSerializer


class CourseRating(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        return Response({"Success": "msb blablabla"}, status=status.HTTP_401_UNAUTHORIZED, headers=None)
        rater = self.request.user.profile

        print('rater', rater)
        course = serializer.validated_data.get('course')
        current_rating = serializer.validated_data.get('rating')

        # print('course.students.all()', not course.students.all().filter(user=self.request.user).exists())
        # print('course.students.all()', course.students.filter(self.request.user.profile).exists())

        # if 

        if rater == course.instructor:
            print('You are the instructor cannoot rate course')
            return

        elif course.students.all().filter(user=self.request.user).exists():

            print('here?')

            total_rate = (course.rating + current_rating) /( course.raters + 1)

            course.rating = total_rate
            course.raters += 1

            course.save()
            serializer.save(rater=rater)

        else:
            print('here')
            return status.HTTP_401_UNAUTHORIZED,
            print('you are not enrolled in the course ')
            return Response({'error': 'you are not enrolled in the course'})

        """
        Dont allow if the 
        rater is not enrolled in the course
        rater is course instructor

        combine the current rating with previous rating
        combine the current rating with previous rating
        """


        # print('serializer', serializer.validated_data)
        # serializer.save()