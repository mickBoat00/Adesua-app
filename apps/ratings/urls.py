from django.urls import path

from .views import CourseRating

# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()

# router.register(r"", CourseRating, basename="ratings")

urlpatterns = [path("", CourseRating.as_view(), name="rate-course")]
# urlpatterns = router.urls
