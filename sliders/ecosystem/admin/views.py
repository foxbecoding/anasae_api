from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from sliders.serializers import *
from pprint import pprint

class AdminSliderViewSet(viewsets.ViewSet):
    def get_permissions(self):
        # permission_classes = [AllowAny]
        permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        serializer = CreateSliderSerializer(data=request.data)
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()
        data = SliderSerializer(instance).data
        return Response(data, status=status.HTTP_201_CREATED)
    
class AdminSliderImageViewSet(viewsets.ViewSet):
    def get_permissions(self):
        # permission_classes = [AllowAny]
        permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        serializer = CreateSliderImageSerializer(data=request.data)
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.create(request.data)
        return Response(data, status=status.HTTP_201_CREATED)