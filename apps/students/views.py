from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import permission_classes

from apps.promotion.models import TrailCourse, UserPromotion
from apps.promotion.serializers import UserPromotionSerializer

from .models import CourseEnrollment
from .permissions import EnrolledStudentPermission
from .serializers import CourseEnrollmentSerializer


class StudentEnrollmentAPIView(generics.CreateAPIView):
    permission_classes = [EnrolledStudentPermission]
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer

    def perform_create(self, serializer):

        course = serializer.validated_data.get("course")

        try:
            x = TrailCourse.courses_on_trail.through.objects.get(Q(trail_id__is_active=True) & Q(course_id=course))

            if x.on_trail == True:
                serializer.save(course_on_free_trail=True, student=self.request.user)

        except ObjectDoesNotExist:
            serializer.save(course_on_free_trail=False, student=self.request.user)


class PromotionActivation(generics.ListCreateAPIView):
    queryset = UserPromotion.objects.all()
    serializer_class = UserPromotionSerializer
