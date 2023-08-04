from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import *
from users.ecosystem.methods import get_user_data
from django.core.mail import EmailMessage
from django.template.loader import get_template
import os
    
class UserAuthLogInViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
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
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    # @method_decorator(csrf_protect)
    def create(self, request):
        self.send_mail(
            request.data['email'],
            'Here is your verification code'
        )
        return Response(None, status=status.HTTP_200_OK) 
    
    def send_mail(self, email, message):
        ctx = {
            'email': email,
            'message': message,
        }

        try:
            msg = EmailMessage(
                'Verify Email',
                get_template(os.getenv('VERIFY_EMAIL_HTML')).render(ctx),
                os.getenv('EMAIL_HOST_USER'),
                [email],
            )
            msg.content_subtype ="html"
            msg.send()
        except Exception as e: 
            print(f'This shit will work soon: {e}')