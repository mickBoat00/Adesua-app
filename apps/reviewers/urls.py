from django.urls import path

from .views import PendingCourseListAPIView, UpdatePendingCoureAPIView

urlpatterns = [
    path("", PendingCourseListAPIView.as_view()),
    path("<slug:slug>/", UpdatePendingCoureAPIView.as_view()),
]
