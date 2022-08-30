from django.urls import path

from .views import PromotionActivation, StudentEnrollmentAPIView

app_name = "student"

urlpatterns = [
    path("course-enrollment/", StudentEnrollmentAPIView.as_view(), name="course-enrollment"),
    path("promotion-activation/", PromotionActivation.as_view(), name="promotion-activation"),
]
