from rest_framework.routers import DefaultRouter
from users.ecosystem.app.views import *

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"user-image", UserImageViewSet, basename="user-image")
router.register(r"user-addresses", UserAddressViewSet, basename="user-address")
router.register(r"user-payment-methods", UserPaymentMethodViewSet, basename="user-payment-method")
urlpatterns = router.urls