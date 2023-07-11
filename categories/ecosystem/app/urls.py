from rest_framework.routers import DefaultRouter
from categories.ecosystem.app.views import *

router = DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
urlpatterns = router.urls