from django.urls import path

from . import views

urlpatterns = [
    path('', views.CourseListAPIView.as_view(), name='course-list'),
    path('<slug:slug>/', views.CourseDetailAPIView.as_view(), name='course-detail'),
]