from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CoursesOnTrailViewset, PromotionModelViewset

app_name = "promotion"
# urlpatterns = [path("", PromotionListCreateAPIView.as_view(), name="promotion-list-create")]


router = DefaultRouter()
router.register(r"create-trial", CoursesOnTrailViewset, basename="trail-list-create")
router.register(r"", PromotionModelViewset, basename="promotion-list-create")
urlpatterns = router.urls
