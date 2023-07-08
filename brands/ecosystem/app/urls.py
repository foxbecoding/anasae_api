from rest_framework.routers import DefaultRouter
from brands.ecosystem.app.views import *

router = DefaultRouter()
router.register(r"brand", BrandViewSet, basename="brand")
urlpatterns = router.urls