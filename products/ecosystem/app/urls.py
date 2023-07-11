from rest_framework.routers import DefaultRouter
from products.ecosystem.app.views import *

router = DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
urlpatterns = router.urls