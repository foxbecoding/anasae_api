from rest_framework.routers import DefaultRouter
from users.ecosystem.app.views import *

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
urlpatterns = router.urls