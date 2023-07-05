from rest_framework.routers import DefaultRouter
from users.ecosystem.authentication.views import *

router = DefaultRouter()
router.register(r"auth-log-in", AccountLogInViewSet, basename="account-log-in")
router.register(r"auth-log-out", AccountLogOutViewSet, basename="account-log-out")
urlpatterns = router.urls