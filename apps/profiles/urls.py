from django.urls import path

from .views import MyProfileAPIView, UpdateMyProfileAPIView, CourseInstructorProfileAPIView

urlpatterns = [
    path('me/', MyProfileAPIView.as_view(), name='my-profile'),
    path('<int:pk>/update/', UpdateMyProfileAPIView.as_view(), name='update-profile'),
    path('<int:pk>/', CourseInstructorProfileAPIView.as_view(), name='instructor-profile'),
    
]