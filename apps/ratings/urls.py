from django.urls import path

from .views import CourseRating

app_name = "ratings"

urlpatterns = [path("", CourseRating.as_view(), name="rate-course")]
