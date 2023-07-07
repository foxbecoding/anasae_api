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

class UserViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        # Create_User_Serializer = CreateUserSerializer(data=request.data, context={'request': request})
        # if not Create_User_Serializer.is_valid():
        #     return Response(Create_User_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        
        # User_Instance = Create_User_Serializer.validated_data['user']
        # data = get_user_data(User_Instance)
        return Response(None, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        # self.check_object_permissions(request=request, obj={'user_pk': pk})
        # data = get_user_data(request.user)
        return Response(None, status=status.HTTP_200_OK)
