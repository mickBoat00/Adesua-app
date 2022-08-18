from django.http import Http404
from rest_framework import generics, permissions, response, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from .models import CoursesOnPromotion, Promotion
from .serializers import PromotionsSerializers  # , CoursesOnPromotionsSerializers,


class InstructorAdminOnly(permissions.BasePermission):
    message = "You are not a course Instructor or an ADMIN."

    """
        Check if the request.user's type is INSTRUCTOR or and ADMIN
    """

    def has_permission(self, request, view):

        if request.user.type == "INSTRUCTOR" or request.user.type == "ADMIN":
            return True


class PromotionListCreateAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, InstructorAdminOnly]
    queryset = Promotion.objects.all()
    serializer_class = PromotionsSerializers

    def list(self, request):
        if request.user.type == "ADMIN":
            queryset = Promotion.objects.all()
        else:
            queryset = Promotion.objects.filter(created_by=request.user)

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
