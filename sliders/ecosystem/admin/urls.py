from rest_framework.routers import DefaultRouter
from .views import SliderViewSet, SliderImageViewSet

router = DefaultRouter()
router.register(r"slider", SliderViewSet, basename="slider")
router.register(r"slider-image", SliderImageViewSet, basename="slider-image")
urlpatterns = router.urls