from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import *
from products.serializers import *
from products.permissions import *
from products.ecosystem.methods import get_product_data
from categories.ecosystem.methods import *
from pprint import pprint

class ProductViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, ProductPermission]
        return [permission() for permission in permission_classes]

    def list(self, request):
        return Response(None, status=status.HTTP_200_OK)
    
    @method_decorator(csrf_protect)
    def create(self, request):
        self.check_object_permissions(request=request, obj={'brand_pk': request.data['brand']})
        Create_Product_Serializer = CreateProductSerializer(data=request.data)
        if not Create_Product_Serializer.is_valid(): return False
        data = ProductSerializer(Create_Product_Serializer.validated_data['product'])
        get_product_data((str(data.id)))
        return Response(None, status=status.HTTP_200_OK)