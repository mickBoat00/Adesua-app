from rest_framework import generics
from rest_framework.decorators import permission_classes

from apps.promotion.models import UserPromotion
from apps.promotion.serializers import UserPromotionSerializer

from .models import CourseEnrollment
from .permissions import EnrolledStudentPermission
from .serializers import CourseEnrollmentSerializer


class StudentEnrollmentAPIView(generics.CreateAPIView):
    permission_classes = [EnrolledStudentPermission]
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class PromotionActivation(generics.ListCreateAPIView):
    queryset = UserPromotion.objects.all()
    serializer_class = UserPromotionSerializer
