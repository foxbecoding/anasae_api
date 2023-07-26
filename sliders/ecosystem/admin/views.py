from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from pprint import pprint

class AdminSliderViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        print('Slider')
        return Response(None, status=status.HTTP_200_OK)
    
class AdminSliderImageViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        print('SliderImage')
        return Response(None, status=status.HTTP_200_OK)