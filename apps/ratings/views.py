from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from apps.course.models import Course

from .models import Rating
from .serializers import RatingSerializer


class CreateRatingsPerm(permissions.BasePermission):
    def has_permission(self, request, view):

        course = Course.objects.get(id=17)

        if course.students.filter(profile=request.user.profile).exists():
            return True


class CourseRating(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    # def create(self, request, *args, **kwargs):

    #     rater = request.user
    #     course = Course.objects.get(id=request.data.get("course"))

    #     if rater == course.instructor:
    #         return Response({"fail": "sorry you cannot rate your own course"}, status=status.HTTP_401_UNAUTHORIZED)

    #     elif course.enrollments.filter(student=rater).exists():

    #         print("re", request.data)

    #         request.data["rater"] = request.user.pkid

    #         print("re", request.data)

    #         serializer = self.get_serializer(data=request.data)

    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #     else:
    #         return Response(
    #             {"error": "you are not a student of this course hence you can't rate the course"},
    #             status=status.HTTP_401_UNAUTHORIZED,
    #         )

    def perform_create(self, serializer):
        return serializer.save(rater=self.request.user)
