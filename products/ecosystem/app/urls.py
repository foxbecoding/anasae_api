from rest_framework.routers import DefaultRouter
from products.ecosystem.app.views import *

router = DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
router.register(r"product-listing", ProductListingViewSet, basename="product-listing")
router.register(r"product-price", ProductPriceViewSet, basename="product-price")
router.register(r"product-image", ProductImageViewSet, basename="product-image")
router.register(r"product-specification", ProductSpecificationViewSet, basename="product-specification")
router.register(r"brand-center-product", BrandCenterProductViewSet, basename="brand-center-product")
urlpatterns = router.urls