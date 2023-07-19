from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from products.models import *
from products.serializers import *
from products.permissions import *
from products.ecosystem.classes import ProductData
from categories.ecosystem.methods import *
from pprint import pprint
from utils.helpers import str_to_list

class ProductViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [ProductPermission]
        needs_auth = ['create','update']
        if self.action in needs_auth: permission_classes = [IsAuthenticated, ProductPermission]
        return [permission() for permission in permission_classes]

    def list(self, request):
        query = request.query_params
        pks = []
        if 'pks' in query: 
            pks = str_to_list(query.get('pks'))
            obj = {'pks': pks, 'action': self.action}
            self.check_object_permissions(request=request, obj=obj)
            data = ProductData(pks, many=True).products
        return Response(data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        data = ProductData([str(pk)]).products
        return Response(data, status=status.HTTP_200_OK)
    
    @method_decorator(csrf_protect)
    def create(self, request):
        self.check_object_permissions(request=request, obj={})
        create_serializer = CreateProductSerializer(data=request.data, many=True)
        
        if not create_serializer.is_valid(): 
            return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = create_serializer.validated_data
        pks = BulkCreateProductSerializer.create(validated_data)
        data = ProductData(pks, many=True).products
        return Response(data, status=status.HTTP_201_CREATED)
    
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'product_pk': pk})
        Product_Instance = Product.objects.get(pk=pk)
        edit_serializer = EditProductSerializer(Product_Instance, data=request.data)
        if not edit_serializer.is_valid(): return Response(edit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        edit_serializer.save()
        data = ProductData([str(pk)]).products
        return Response(data, status=status.HTTP_202_ACCEPTED)
    
class ProductPriceViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, ProductPricePermission]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        create_serializer = CreateProductPriceSerializer(data=request.data, many=True)
        if not create_serializer.is_valid(): return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = create_serializer.validated_data
        data = BulkCreateProductPriceSerializer.create(validated_data)
        return Response(data, status=status.HTTP_201_CREATED)
    
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'product_price_pk': pk})
        Product_Price_Instance = ProductPrice.objects.get(pk=pk)
        edit_serializer = EditProductPriceSerializer(Product_Price_Instance, request.data)
        if not edit_serializer.is_valid(): return Response(edit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        validated_data = edit_serializer.validated_data
        data = edit_serializer.update(Product_Price_Instance, validated_data)
        return Response(data, status=status.HTTP_202_ACCEPTED)

class ProductSpecificationViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, ProductSpecificationPermission]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        create_serializer = CreateProductSpecificationSerializer(data=request.data, many=True)
        if not create_serializer.is_valid(): return Response(None, status=status.HTTP_400_BAD_REQUEST)
        data = BulkCreateProductSpecificationSerializer.create(create_serializer.validated_data)
        return Response(data, status=status.HTTP_201_CREATED)
    
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        pks = str_to_list(pk)
        instances = ProductSpecification.objects.filter(pk__in=pks)
        edit_serializer = EditProductPriceSerializer(instances, data=request.data, many=True)
        if not edit_serializer.is_valid(): return Response(edit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(edit_serializer.validated_data)
        # return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(None, status=status.HTTP_202_ACCEPTED)