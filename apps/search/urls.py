from django.urls import path

from .views import SearchCourse

urlpatterns = [
    path('<str:query>/', SearchCourse.as_view()),
]