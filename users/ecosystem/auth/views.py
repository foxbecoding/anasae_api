from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import *
from users.ecosystem.methods import get_user_data
from users.models import UserVerifyEmail
from django.core.mail import EmailMessage
from django.template.loader import get_template
from utils.helpers import key_exists
import os, pyotp
    
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
        if key_exists(request.data['otp_code']):
            if not UserVerifyEmail.objects.filter(email=email).filter(otp_code=otp_code).exists():
                return Response({'error': 'An error has occured.'}, status=status.HTTP_400_BAD_REQUEST)
            
            instance = UserVerifyEmail.objects.get(email=email)
            if instance.otp_code != request.data['otp_code']:
                return Response({'error': 'Verification failed, please try again.'}, status=status.HTTP_400_BAD_REQUEST)
            
            instance.verified_status = True
            instance.save()
            
            return Response({'success': 'Email verified!'}, status=status.HTTP_202_ACCEPTED)

        email, otp_code = [ request.data['email'], pyotp.TOTP('base32secret3232').now() ]

        if not UserVerifyEmail.objects.filter(email=email).exists():
            instance = UserVerifyEmail.objects.create(
                email=email,
                otp_code=otp_code,
                verified_status=False
            )
            instance.save()
        else:
            instance = UserVerifyEmail.objects.get(email=email)
            instance.otp_code = otp_code
            instance.save()

        ctx = {
            'message': 'Verification code',
            'message2': 'Use this code to complete your account creation.',
            'otp_code': otp_code,
            'logo': os.getenv('EMAIL_LOGO')
        }

        self.send_mail(email, ctx)
        return Response(None, status=status.HTTP_200_OK) 
    
    def send_mail(self, email, ctx):
        try:
            msg = EmailMessage(
                'Verify Email',
                get_template(os.getenv('VERIFY_EMAIL_HTML')).render(ctx),
                os.getenv('NO_REPLY_EMAIL'),
                [email],
            )
            msg.content_subtype ="html"
            msg.send()
        except Exception as e: print(e)