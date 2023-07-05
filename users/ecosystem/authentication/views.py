from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import *
    
class AccountLogInViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        Account_Login_Serializer = UserAuthSerializer(data=request.data, context={ 'request': request })
        
        if not Account_Login_Serializer.is_valid():
            return Response(Account_Login_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = Account_Login_Serializer.validated_data['user']
        login(request, user)
        
        User_Login_Serializer = UserLoginSerializer(data={'user': user.id})
        if User_Login_Serializer.is_valid(): User_Login_Serializer.save()
        User_Serializer = UserSerializer(user)
        
        return Response(User_Serializer.data, status=status.HTTP_202_ACCEPTED)
    
class AccountLogOutViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        logout(request)
        return Response(None, status=status.HTTP_200_OK) 