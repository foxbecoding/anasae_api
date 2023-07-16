from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import *
from products.serializers import *
from products.permissions import *
from products.ecosystem.classes import ProductData
from categories.ecosystem.methods import *
from pprint import pprint

class ProductViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [ProductPermission]
        needs_auth = ['create','update']
        if self.action in needs_auth: permission_classes = [IsAuthenticated, ProductPermission]
        return [permission() for permission in permission_classes]

    def list(self, request):
        return Response(None, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        data = ProductData([str(pk)]).products
        return Response(data, status=status.HTTP_200_OK)
    
    @method_decorator(csrf_protect)
    def create(self, request):
        self.check_object_permissions(request=request, obj={})
        Create_Product_Serializer = CreateProductSerializer(data=request.data, context={'request': request}, many=True)
        
        if not Create_Product_Serializer.is_valid(): 
            return Response(Create_Product_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = Create_Product_Serializer.validated_data
        pks = BulkCreateProductSerializer.create(validated_data)
        data = ProductData(pks, many=True).products
        return Response(data, status=status.HTTP_201_CREATED)
    
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'product_pk': pk})
        Product_Instance = Product.objects.get(pk=pk)
        Edit_Product_Serializer = EditProductSerializer(Product_Instance, data=request.data)
        
        if not Edit_Product_Serializer.is_valid(): 
            return Response(Edit_Product_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Edit_Product_Serializer.save()
        data = ProductData([str(pk)]).products
        return Response(data, status=status.HTTP_202_ACCEPTED)
    
class ProductPriceViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = []
        needs_auth = ['create','update']
        if self.action in needs_auth: permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    # def retrieve(self, request, pk=None):
    #     data = ProductData([str(pk)]).products
    #     return Response(data, status=status.HTTP_200_OK)
    
    @method_decorator(csrf_protect)
    def create(self, request):
        print(request.data)
        return Response(None, status=status.HTTP_201_CREATED)
    
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        return Response(None, status=status.HTTP_202_ACCEPTED)