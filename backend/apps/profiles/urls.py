from django.urls import path

from .views import (
    CourseInstructorProfileAPIView,
    MyProfileAPIView,
    UpdateMyProfileAPIView,
)

urlpatterns = [
    path("me/", MyProfileAPIView.as_view(), name="my-profile"),
    path("<int:pk>/update/", UpdateMyProfileAPIView.as_view(), name="update-profile"),
    path("<int:pk>/", CourseInstructorProfileAPIView.as_view(), name="instructor-profile"),
]
