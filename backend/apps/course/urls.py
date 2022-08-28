from django.urls import include, path
from rest_framework import routers

from .views import CourseModelViewset, LessonModelViewset

# from . import views

app_name = "course"

# urlpatterns = [
#     path("courses/", views.CourseListAPIView.as_view(), name="course-list"),
#     path("courses/create/", views.CourseCreateAPIView.as_view(), name="course-create"),
#     path("courses/<slug:slug>/", views.CourseDetailAPIView.as_view(), name="course-detail"),
#     path("courses/<slug:slug>/lessons/", views.CourseLessonsAPIView.as_view(), name="course-lesson"),
#     path("lessons/<slug:slug>/", views.LessonDetailAPIView.as_view(), name="lesson-detail"),
# ]


router = routers.SimpleRouter()

router.register(r"courses", CourseModelViewset, basename="courses")
router.register(r"courses/(?P<courseslug>[^/.]+)/lessons", LessonModelViewset, basename="lessons")


urlpatterns = router.urls
