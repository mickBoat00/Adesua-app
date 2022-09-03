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
    path("reviewers/", PendingCourseListAPIView.as_view(), name="pending-courses"),
    path("reviewers/", include(router.urls)),
    path("reviewers/<slug:slug>/", UpdatePendingCoureAPIView.as_view()),
]
