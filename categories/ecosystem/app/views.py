from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from categories.models import *
from categories.serializers import *
from pprint import pprint

class CategoryViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request):
        return Response(None, status=status.HTTP_200_OK)
