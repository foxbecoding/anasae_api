from rest_framework.routers import DefaultRouter
from categories.ecosystem.app.views import *

router = DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(
    r"category-product-specifications", 
    CategoryProductSpecificationViewSet, 
    basename="category-product-specification"
)
router.register(
    r"category-page", 
    CategoryPageViewSet, 
    basename="category-page"
)
router.register(
    r"category-home-page", 
    CategoryHomePageViewSet, 
    basename="category-home-page"
)
urlpatterns = router.urls