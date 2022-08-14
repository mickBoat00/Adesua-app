from django.urls import path

from .views import StudentEnrollmentAPIView  # , StudentSignUpAPIView

urlpatterns = [
    # path("", StudentSignUpAPIView.as_view()),
    path("course-enrollment/", StudentEnrollmentAPIView.as_view()),
]
