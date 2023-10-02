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
from products.ecosystem.classes import ProductData, ProductListingView
from utils.helpers import str_to_list

class ProductListingViewSet(viewsets.ViewSet):
    lookup_field = 'uid'
    def get_permissions(self):
        permission_classes = [IsAuthenticated, ProductListingPermission]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        user_id = str(request.user.id)
        data = ProductListingView().listView(user_id)
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, uid=None):
        self.check_object_permissions(request, obj={'uid': uid})
        data = ProductListingView().retrieveView(uid)
        return Response(data, status=status.HTTP_200_OK)

    @method_decorator(csrf_protect)
    def partial_update(self, request, uid=None):
        self.check_object_permissions(request, obj={'uid': uid})
        instance = ProductListing.objects.get(uid=uid)
        serializer = EditProductListingSerializer(instance, request.data)
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user_id = str(request.user.id)
        data = ProductListingView().listView(user_id)
        return Response(data, status=status.HTTP_202_ACCEPTED)

class ProductListingBaseVariantViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, ProductListingBaseVariantPermission]
        return [permission() for permission in permission_classes]
    
    def update(self, request, pk=None):
        self.check_object_permissions(request, obj = {'pk': pk})
        user_id = str(request.user.id)
        instance = ProductListingBaseVariant.objects.get(pk=pk)
        edit_serializer = EditProductListingBaseVariantSerializer(instance, request.data)
        if not edit_serializer.is_valid(): return Response(edit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        edit_serializer.save()
        data = ProductListingView().listView(user_id)
        return Response(data, status=status.HTTP_202_ACCEPTED)

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
        permission_classes = [IsAuthenticated, ProductDimensionPermission]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        user_id = str(request.user.id)
        if not Brand.objects.filter(creator = user_id).exists(): 
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        
        create_serializer = CreateProductDimensionSerializer(data=request.data, many=True)
        if not create_serializer.is_valid(): return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = create_serializer.validated_data
        data = BulkCreateProductDimensionSerializer.create(validated_data)
        return Response(data, status=status.HTTP_201_CREATED)
    
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        user_id = str(request.user.id)
        if not Brand.objects.filter(creator = user_id).exists(): 
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        Product_Dimension_Instance = ProductDimension.objects.get(pk=pk)
        self.check_object_permissions(request, {'instance': Product_Dimension_Instance})
        edit_serializer = EditProductDimensionSerializer(Product_Dimension_Instance, request.data)
        if not edit_serializer.is_valid(): return Response(edit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        data =  ProductDimensionSerializer(edit_serializer.save()).data
        return Response(data, status=status.HTTP_202_ACCEPTED)