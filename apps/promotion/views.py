from django.http import Http404
from rest_framework import generics, permissions, response, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from .models import CoursesOnPromotion, Promotion, TrialCourse
from .serializers import (
    CoursesOnTrailSerializer,
    PromotionsSerializers,
)

from .permissions import InstructorAdminOnly


class PromotionModelViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, InstructorAdminOnly]
    queryset = Promotion.objects.all()
    serializer_class = PromotionsSerializers

    def list(self, request):
        if request.user.type == "ADMIN":
            queryset = Promotion.objects.select_related("coupon")
        else:
            queryset = Promotion.objects.select_related("coupon").filter(created_by=request.user)

        serializer = PromotionsSerializers(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = Promotion.objects.filter(created_by=request.user)

        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.queryset = Promotion.objects.filter(created_by=request.user)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.get_object().user == request.user:
            return super().destroy(request, *args, **kwargs)
        else:
            raise Http404

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CoursesOnTrailViewset(viewsets.ModelViewSet):
    queryset = TrialCourse.objects.all()
    serializer_class = CoursesOnTrailSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
