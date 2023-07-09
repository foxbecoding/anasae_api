from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from brands.models import *
from brands.serializers import *
from brands.permissions import *
from brands.ecosystem.methods import *
from pprint import pprint

class BrandViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, BrandPermission]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        Create_Brand_Serializer = CreateBrandSerializer(data=request.data, context={'request': request})
        if not Create_Brand_Serializer.is_valid():
            return Response(Create_Brand_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        
        Brand_Instance = Create_Brand_Serializer.validated_data['brand']
        data = get_brand_data(Brand_Instance)
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'brand_pk': pk})
        Brand_Instance = Brand.objects.get(pk=pk)
        data = get_brand_data(Brand_Instance)
        return Response(data, status=status.HTTP_200_OK)
    
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'brand_pk': pk})
        Brand_Instance = Brand.objects.get(pk=pk)
        
        Edit_Brand_Serializer = EditBrandSerializer(Brand_Instance, data=request.data)
        if not Edit_Brand_Serializer.is_valid():
            return Response(Edit_Brand_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        Edit_Brand_Serializer.save()
        data = get_brand_data(Brand_Instance)
        return Response(data, status=status.HTTP_202_ACCEPTED)

class BrandLogoViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, BrandLogoPermission]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        brand_pk = str(request.data['brand'])
        is_brand_logo = BrandLogo.objects.filter(brand_id=brand_pk).exists()
        if is_brand_logo:
            Brand_Logo = BrandLogo.objects.get(brand_id=brand_pk)
            # remove image from cdn maybe??? idk yet
            Brand_Logo.delete()

        Create_Brand_Logo_Serializer = CreateBrandLogoSerializer(data={'brand': brand_pk}, context={ 'request': request })
        if not Create_Brand_Logo_Serializer.is_valid():
            return Response(Create_Brand_Logo_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = get_brand_data(Create_Brand_Logo_Serializer.validated_data['brand'])
        return Response(data, status=status.HTTP_201_CREATED)
    
class BrandOwnerViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, BrandOwnerPermission]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        Create_Brand_Owner_Serializer = CreateBrandOwnerSerializer(data=request.data)
        if not Create_Brand_Owner_Serializer.is_valid():
            return Response(Create_Brand_Owner_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Brand_Instance = Brand.objects.get(creator_id=str(request.user.id))
        data = get_brand_data(Brand_Instance)
        return Response(data, status=status.HTTP_201_CREATED)
    
    @method_decorator(csrf_protect)
    def destroy(self, request):
        return Response(None, status=status.HTTP_201_CREATED)
    
class BrandFollowerViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        # Create_Brand_Owner_Serializer = CreateBrandOwnerSerializer(data=request.data)
        # if not Create_Brand_Owner_Serializer.is_valid():
        #     return Response(Create_Brand_Owner_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Brand_Instance = Brand.objects.get(creator_id=str(request.user.id))
        # data = get_brand_data(Brand_Instance)
        # return Response(data, status=status.HTTP_201_CREATED)
        return Response(None, status=status.HTTP_201_CREATED)