from rest_framework import generics, permissions
from rest_framework.decorators import permission_classes

from .models import Profile
from .serializers import (
    InstructorProfileSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
)


class MyProfileAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request

        return qs.filter(user=request.user)


class UpdateMyProfileAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UpdateProfileSerializer

    def perform_update(self, serializer):

        return super().perform_update(serializer)


class CourseInstructorProfileAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = InstructorProfileSerializer
