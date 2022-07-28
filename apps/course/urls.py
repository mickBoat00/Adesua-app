from django.urls import path

from . import views

urlpatterns = [
    path('courses/', views.CourseListAPIView.as_view(), name='course-list'),
    path('courses/create/', views.CourseCreateAPIView.as_view(), name='course-create'),
    path('course/<slug:slug>/', views.CourseDetailAPIView.as_view(), name='course-detail'),
    path('lessons/create/', views.LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/<slug:slug>/', views.LessonDetailAPIView.as_view(), name='lesson-detail'),
    
]