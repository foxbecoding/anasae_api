from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from categories.models import *
from categories.serializers import *
from categories.ecosystem.classes import *
from pprint import pprint
import random 

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
        if not CategoryProductSpecification.objects.filter(pk=pk).exists():
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        instance = CategoryProductSpecification.objects.get(pk=pk)
        serializer_data = CategoryProductSpecificationSerializer(instance).data
        instances = CategoryProductSpecificationItem.objects.filter(pk__in=serializer_data['items'])
        specifications = CategoryProductSpecificationItemSerializer(instances, many=True).data
        for spec in specifications:
            options_ins = CategoryProductSpecificationItemOption.objects.filter(pk__in=spec['options'])
            options = [item['option'] for item in CategoryProductSpecificationItemOptionSerializer(options_ins, many=True).data]
            spec['options'] = options
        return Response(specifications, status=status.HTTP_200_OK)
    
class CategoryPageViewSet(viewsets.ViewSet):
    lookup_field = 'uid'
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, uid=None):
        if not Category.objects.filter(uid=uid): return Response(None, status=status.HTTP_404_NOT_FOUND)
        data = CategoryPageView().retrieveView(uid)
        return Response(data, status=status.HTTP_200_OK)

class CategoryHomePageViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request):
        data = CategoryHomePageView().listView()
        return Response(data, status=status.HTTP_200_OK)
