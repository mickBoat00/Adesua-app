from django.urls import path

from .views import StudentEnrollmentAPIView

app_name = "student"

urlpatterns = [
    path("course-enrollment/", StudentEnrollmentAPIView.as_view(), name="course-enrollment"),
]
