from django.urls import include, path
from rest_framework import routers

from .views import CourseRatingModelViewset

app_name = "ratings"

router = routers.SimpleRouter()

router.register(r"courses/(?P<courseslug>[^/.]+)/ratings", CourseRatingModelViewset, basename="course-rating")

urlpatterns = router.urls
