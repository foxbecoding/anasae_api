from rest_framework.routers import DefaultRouter
from products.ecosystem.app.views import *

router = DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
router.register(r"product-listing", ProductListingViewSet, basename="product-listing")
router.register(r"product-listing-page", ProductListingPageViewSet, basename="product-listing-page")
router.register(r"product-listing-base-variant", ProductListingBaseVariantViewSet, basename="product-listing-base-variant")
router.register(r"product-dimension", ProductDimensionViewSet, basename="product-dimension")
router.register(r"product-price", ProductPriceViewSet, basename="product-price")
router.register(r"product-image", ProductImageViewSet, basename="product-image")
router.register(r"product-specification", ProductSpecificationViewSet, basename="product-specification")
urlpatterns = router.urls