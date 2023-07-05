from rest_framework.routers import DefaultRouter
from users.ecosystem.authentication.views import *

router = DefaultRouter()
router.register(r"auth-log-in", UserAuthLogInViewSet, basename="account-log-in")
router.register(r"auth-log-out", UserAuthLogOutViewSet, basename="account-log-out")
urlpatterns = router.urls