from django.urls import path

from .views import PayCourseAPIView

urlpatterns = [
    path('ordered/', PayCourseAPIView.as_view(), name='pay-course'), 
]