from rest_framework.routers import DefaultRouter
from .views import SliderViewSet

router = DefaultRouter()
router.register(r"slider", SliderViewSet, basename="slider")
urlpatterns = router.urls