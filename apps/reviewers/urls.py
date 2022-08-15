from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminCreateReviewers,
    PendingCourseListAPIView,
    UpdatePendingCoureAPIView,
)

router = DefaultRouter()

router.register(r"add-reviewers", AdminCreateReviewers, basename="reviewers")

app_name = "reviewer"

urlpatterns = [
    path("", PendingCourseListAPIView.as_view(), name="pending-courses"),
    path("", include(router.urls)),
    path("<slug:slug>/", UpdatePendingCoureAPIView.as_view()),
]
