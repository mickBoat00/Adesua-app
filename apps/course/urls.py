from django.urls import include, path
from rest_framework import routers

from .views import CourseModelViewset, LessonModelViewset

app_name = "course"

router = routers.DefaultRouter()

router.register(r"courses", CourseModelViewset, basename="courses")
router.register(r"courses/(?P<courseslug>[^/.]+)/lessons", LessonModelViewset, basename="lessons")


urlpatterns = router.urls
