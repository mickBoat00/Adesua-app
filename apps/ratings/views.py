from rest_framework import generics, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from .models import Rating
from .serializers import RatingSerializer


class CourseRating(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        rater = self.request.user.profile

        print("rater", rater)

        course = serializer.validated_data.get("course")

        if rater == course.instructor:
            print("You are the instructor cannoot rate course")
            return Response(
                {"Success": "msb blablabla"},
                status.HTTP_401_UNAUTHORIZED,
            )

        elif course.students.filter(profile=rater).exists():

            print("yesss")

            serializer.save(rater=rater)

        else:
            print("Nope")
            return Response(
                {"Success": "msb blablabla"},
                status.HTTP_401_UNAUTHORIZED,
            )
