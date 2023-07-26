from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from sliders.serializers import *
from sliders.models import *
from pprint import pprint

class SliderViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        if not Slider.objects.filter(pk=pk).exists: return Response([], status=status.HTTP_200_OK)
        instance = Slider.objects.get(pk=pk)
        data = SliderSerializer(instance).data
        return Response(data, status=status.HTTP_200_OK)