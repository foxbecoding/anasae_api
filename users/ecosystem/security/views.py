from django.middleware.csrf import get_token
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

    
class ForceCSRFViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        get_token(request)
        return Response(None, status=status.HTTP_200_OK)