from rest_framework.routers import DefaultRouter
from products.ecosystem.app.views import *

router = DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
router.register(r"product-price", ProductPriceViewSet, basename="product-price")
urlpatterns = router.urls