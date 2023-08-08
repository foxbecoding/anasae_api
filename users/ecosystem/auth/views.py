from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import *
from users.permissions import *
from users.ecosystem.methods import get_user_data
from users.models import UserVerifyEmail
from utils.helpers import key_exists
    
class UserAuthLogInViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        if key_exists('email', request.data):
            User_Auth_Serializer = UserAuthEmailSerializer(data=request.data, context={ 'request': request })
        else:
            User_Auth_Serializer = UserAuthSerializer(data=request.data, context={ 'request': request })
        
        if not User_Auth_Serializer.is_valid():
            return Response(User_Auth_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = User_Auth_Serializer.validated_data['user']
        login(request, user)
    
        data = get_user_data(user)
        return Response(data, status=status.HTTP_202_ACCEPTED)
    
class UserAuthLogOutViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        logout(request)
        return Response(None, status=status.HTTP_200_OK) 
    
class UserAuthValidateViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        serializer = UserAuthValidateSerializer(data=request.data)
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class UserAuthValidateDetailsViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        serializer = UserAuthValidateDetailsSerializer(data=request.data)
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_202_ACCEPTED)
    
class UserAuthValidatePasswordViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        serializer = UserAuthValidatePasswordSerializer(data=request.data)
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_202_ACCEPTED)
    
class UserAuthVerifyEmailViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny, UserAuthVerifyEmailPermission]
        return [permission() for permission in permission_classes]


    # @method_decorator(csrf_protect)
    def create(self, request):
        serializer = CreateUserAuthVerifyEmailSerializer(data=request.data)
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        data = serializer.create(validated_data)
        return Response(data, status=status.HTTP_200_OK) 
    
    # @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        self.check_object_permissions(request, {'pk': pk})
        instance = UserVerifyEmail.objects.get(pk=pk)
        serializer = EditUserAuthVerifyEmailSerializer(data=request.data)
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        data = serializer.update(instance, validated_data)
        return Response(data, status=status.HTTP_202_ACCEPTED)