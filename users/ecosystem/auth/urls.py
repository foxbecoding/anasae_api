from rest_framework.routers import DefaultRouter
from users.ecosystem.auth.views import *

router = DefaultRouter()
router.register(r"auth-log-in", UserAuthLogInViewSet, basename="auth-log-in")
router.register(r"auth-log-out", UserAuthLogOutViewSet, basename="auth-log-out")
urlpatterns = router.urls