from django.urls import path

from . import views

urlpatterns = [
    path('courses/', views.CourseListAPIView.as_view(), name='course-list'),
    path('course/<slug:slug>/', views.CourseDetailAPIView.as_view(), name='course-detail'),
    path('lessons/', views.LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<slug:slug>/', views.LessonDetailAPIView.as_view(), name='lesson-list'),
    
]