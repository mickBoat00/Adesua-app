from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.CourseListAPIView.as_view(), name="course-list"),
    path("course-instructor-signup/", views.CourseInstructorSignUp.as_view(), name="course-instructor-signup"),
    path("courses/create/", views.CourseCreateAPIView.as_view(), name="course-create"),
    path("courses/<slug:slug>/", views.CourseDetailAPIView.as_view(), name="course-detail"),
    path("courses/<slug:slug>/lessons/", views.CourseLessonsAPIView.as_view(), name="course-lesson"),
    path("lessons/<slug:slug>/", views.LessonDetailAPIView.as_view(), name="lesson-detail"),
]
