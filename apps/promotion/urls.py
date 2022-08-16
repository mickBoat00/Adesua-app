from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PromotionListCreateAPIView

app_name = "promotion"
# urlpatterns = [path("", PromotionListCreateAPIView.as_view(), name="promotion-list-create")]


router = DefaultRouter()
router.register(r"", PromotionListCreateAPIView, basename="promotion-list-create")
urlpatterns = router.urls
