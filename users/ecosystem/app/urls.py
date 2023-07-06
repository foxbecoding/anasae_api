from rest_framework.routers import DefaultRouter
from users.ecosystem.app.views import *

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"user-image", UserImageViewSet, basename="user-image")
urlpatterns = router.urls