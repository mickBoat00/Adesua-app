from django.urls import path

from . import views

urlpatterns = [
    path('', views.CourseListAPIView.as_view(), name='course-list'),
    path('<slug:slug>/', views.CourseDetailAPIView.as_view(), name='course-detail'),
    path('<slug:slug>/lessons/', views.CourseLessonListAPIView.as_view(), name='course-lessons'),
    path('<slug:course_slug>/lessons/<slug:lesson_slug>/', views.CourseLessonDetailAPIView.as_view(), name='course-lesson-detail'),
    path('<slug:slug>/lessons/<slug:lesson_slug>/edit/', views.CourseLessonUpdateAPIView.as_view(), name='course-lesson-edit'),
]