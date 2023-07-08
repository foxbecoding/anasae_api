from rest_framework.routers import DefaultRouter
from brands.ecosystem.app.views import *

router = DefaultRouter()
router.register(r"brand", BrandViewSet, basename="brand")
router.register(r"brand-logo", BrandLogoViewSet, basename="brand-logo")
urlpatterns = router.urls