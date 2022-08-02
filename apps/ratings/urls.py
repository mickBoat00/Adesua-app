from django.urls import path

from .views import CourseRating

urlpatterns = [path("", CourseRating.as_view(), name='rate-course')]
