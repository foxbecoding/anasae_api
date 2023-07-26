from rest_framework.routers import DefaultRouter
from .views import AdminSliderViewSet, AdminSliderImageViewSet

router = DefaultRouter()
router.register(r"admin-slider", AdminSliderViewSet, basename="admin-slider")
router.register(r"admin-slider-image", AdminSliderImageViewSet, basename="admin-slider-image")
urlpatterns = router.urls