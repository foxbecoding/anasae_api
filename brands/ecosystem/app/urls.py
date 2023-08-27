from rest_framework.routers import DefaultRouter
from brands.ecosystem.app.views import *

router = DefaultRouter()
router.register(r"brand", BrandViewSet, basename="brand")
router.register(r"brand-logo", BrandLogoViewSet, basename="brand-logo")
router.register(r"brand-owner", BrandOwnerViewSet, basename="brand-owner")
router.register(r"brand-follower", BrandFollowerViewSet, basename="brand-follower")
router.register(r"brand-page", BrandPageViewSet, basename="brand-page")
urlpatterns = router.urls