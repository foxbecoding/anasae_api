from rest_framework.routers import DefaultRouter
from users.ecosystem.security.views import *

router = DefaultRouter()
router.register(r"x-fct", ForceCSRFViewSet, basename="x-fct")
urlpatterns = router.urls