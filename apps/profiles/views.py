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

        # if request.user is not the profile owner
        # do not allow update

        print("serializer", serializer)
        # print('serializer first',serializer[0])
        # print('serializer.validated_data',serializer.validated_data)

        return super().perform_update(serializer)


class CourseInstructorProfileAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = InstructorProfileSerializer
