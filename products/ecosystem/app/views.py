from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from products.models import *
from brands.models import Brand
from products.serializers import *
from products.permissions import *
from products.ecosystem.classes import ProductData
from categories.ecosystem.methods import *
from pprint import pprint
from utils.helpers import str_to_list

class ProductListingViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        user_id = str(request.user.id)
        if not Brand.objects.filter(creator = str(request.user.id)).exists(): 
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        brand_id = str(Brand.objects.get(creator = str(user_id)).id)
        product_listing_ins = ProductListing.objects.filter(brand_id=brand_id)
        data = ProductListingSerializer(product_listing_ins, many=True).data
        return Response(data, status=status.HTTP_200_OK)

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
        self.check_object_permissions(request=request, obj={"pks": pks})
        instances = ProductSpecification.objects.filter(pk__in=pks)
        edit_serializer = EditProductSpecificationSerializer(data=request.data, many=True)
        if not edit_serializer.is_valid(): return Response(edit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = BulkEditProductSpecificationSerializer(instances, edit_serializer.validated_data).specifications
        return Response(data, status=status.HTTP_202_ACCEPTED)
    
class ProductImageViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        # permission_classes = [IsAuthenticated, ProductImagePermission]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        create_serializer = CreateProductImageSerializer(data=request.data)
        if not create_serializer.is_valid(): return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = create_serializer.validated_data
        data = BulkCreateProductImageSerializer(validated_data).product_images
        return Response(data, status=status.HTTP_201_CREATED)
    
    @method_decorator(csrf_protect)
    def destroy(self, request, pk=None):
        pks = str_to_list(pk)
        self.check_object_permissions(request=request, obj={"image_pks": pks})
        instances = ProductImage.objects.filter(pk__in=pks)
        instances.delete()
        return Response(None, status=status.HTTP_202_ACCEPTED)
    

class ProductDimensionViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        user_id = str(request.user.id)
        if not Brand.objects.filter(creator = user_id).exists(): 
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        # create_serializer = CreateProductPriceSerializer(data=request.data, many=True)
        # if not create_serializer.is_valid(): return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # validated_data = create_serializer.validated_data
        # data = BulkCreateProductPriceSerializer.create(validated_data)
        return Response(None, status=status.HTTP_201_CREATED)
        # return Response(data, status=status.HTTP_201_CREATED)
    
    # @method_decorator(csrf_protect)
    # def update(self, request, pk=None):
    #     self.check_object_permissions(request=request, obj={'product_price_pk': pk})
    #     Product_Price_Instance = ProductPrice.objects.get(pk=pk)
    #     edit_serializer = EditProductPriceSerializer(Product_Price_Instance, request.data)
    #     if not edit_serializer.is_valid(): return Response(edit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    #     validated_data = edit_serializer.validated_data
    #     data = edit_serializer.update(Product_Price_Instance, validated_data)
    #     return Response(data, status=status.HTTP_202_ACCEPTED)
        
class BrandCenterProductViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        user_id = str(request.user.id)
        if not Brand.objects.filter(creator = str(request.user.id)).exists(): 
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        brand_id = str(Brand.objects.get(creator = str(user_id)).id)
        product_ins = Product.objects.filter(brand_id=brand_id)
        product_pks = [ str(prod.id) for prod in product_ins]
        data = ProductData(product_pks, many=True).products
        return Response(data, status=status.HTTP_200_OK)