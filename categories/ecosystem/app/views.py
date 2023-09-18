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
        instances = Category.objects.all()
        serializer_data = CategorySerializer(instances, many=True).data
        return Response(serializer_data, status=status.HTTP_200_OK)

class CategoryProductSpecificationViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        print(pk)
        return Response(None, status=status.HTTP_200_OK)
        # return Response(serializer_data, status=status.HTTP_200_OK)
