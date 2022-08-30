from rest_framework import viewsets
from rest_framework.decorators import permission_classes

from apps.course.models import Course

from .models import Rating
from .permissions import CourseRatingPerm
from .serializers import RatingCreateSerializer, RatingReadSerializer


class CourseRatingModelViewset(viewsets.ModelViewSet):
    permission_classes = [CourseRatingPerm]
    queryset = Rating.objects.all()

    def get_queryset(self):
        course = Course.objects.get(slug=self.kwargs.get("courseslug"))
        return self.queryset.filter(course=course)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RatingReadSerializer
        return RatingCreateSerializer

    def perform_create(self, serializer):
        course = Course.objects.get(slug=self.kwargs.get("courseslug"))
        user = self.request.user
        return serializer.save(course=course, rater=user)
