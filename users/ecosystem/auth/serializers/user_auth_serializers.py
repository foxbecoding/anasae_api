from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from django.core.mail import EmailMessage
from django.template.loader import get_template
from users.models import *
import os, pyotp, re

env = os.getenv

class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=True,
        write_only=True
    )

    def validate(self, attrs):
        # Set username and password from attrs
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:

            # Find user with username and password combination
            user = self.authenticate(username, password)
    
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Invalid authentication credentials.'
                raise serializers.ValidationError({"errors": msg}, code='authorization')

        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError({"errors": msg}, code='authorization')

        User_Login_Instance = UserLogin.objects.create(user = user)
        User_Login_Instance.save()
        
        attrs['user'] = user
        return attrs
    
    def authenticate(self, username, password) -> User:
        if not User.objects.filter(username=username).exists(): return None
        User_Instance = User.objects.get(username=username)  
        if not check_password(password, User_Instance.password): return None
        return User_Instance
    
class UserAuthEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    email = serializers.EmailField(
        label="Email",
        write_only=True
    )
    
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=True,
        write_only=True
    )

    def validate(self, attrs):
        # Set email and password from attrs
        email = attrs.get('email')
        password = attrs.get('password')
       
        if email and password:

            # Find user with email and password combination
            user = self.authenticate(email, password)
    
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Invalid authentication credentials.'
                raise serializers.ValidationError({"errors": msg}, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError({"errors": msg}, code='authorization')

        User_Login_Instance = UserLogin.objects.create(user = user)
        User_Login_Instance.save()
        
        attrs['user'] = user
        return attrs
    
    def authenticate(self, email, password) -> User:
        if not User.objects.filter(email=email).exists():
            return None
        User_Instance = User.objects.get(email=email)     
        if not check_password(password, User_Instance.password):
            return None
        return User_Instance

class UserAuthValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]

    def validate(self, attrs):
        username = attrs.get('username').lower()
        email = attrs.get('email').lower()
       
        if User.objects.filter(username=username).exists():
            msg = 'user with this username already exists'
            raise serializers.ValidationError({'username': msg}, code='authorization')
        
        if not re.match("^[A-Za-z0-9_-]*$", username):
            msg = 'Only letters, numbers and underscores are allowed'
            raise serializers.ValidationError({"username": msg}, code='authorization')

        if User.objects.filter(email=email).exists():
            msg = 'user with this email already exists.'
            raise serializers.ValidationError({'email': msg}, code='authorization')
        
        return attrs
    
class UserAuthValidateDetailsSerializer(serializers.ModelSerializer):
    birth_month = serializers.CharField(write_only=True)
    birth_day = serializers.CharField(write_only=True)
    birth_year = serializers.CharField(write_only=True)
    gender = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'birth_month',
            'birth_day',
            'birth_year',
            'gender'
        ]
    
    def validate(self, attrs):
        gender = attrs.get('gender')
       
        if not UserGender.objects.filter(pk=gender).exists():
            msg = 'Gender invalid'
            raise serializers.ValidationError({'gender': msg}, code='authorization')
        
        return attrs

class UserAuthValidatePasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'password',
            'confirm_password'
        ]
    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        # Check if passwords matches
        if password != confirm_password:
            msg = 'Passwords must match.'
            raise serializers.ValidationError({"password": msg}, code='authorization')
        
        return attrs

class UserAuthVerifyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerifyEmail
        fields = [
            'pk',
            'email',
            'otp_code'
        ]

class EditUserAuthVerifyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerifyEmail
        fields = [
            'email',
            'otp_code'
        ]

    def validate(self, attrs):
        email, otp_code = [ attrs.get('email').lower(), attrs.get('otp_code') ]
        if not UserVerifyEmail.objects.filter(email=email).filter(otp_code=otp_code).exists():
            msg = 'Email verification failed, please try again.'
            raise serializers.ValidationError({'error': msg}, code='authorization')
        return attrs
    
    def update(self, instance: UserVerifyEmail, validated_data):
        instance.verified_status = True
        instance.save()
        return {'pk': instance.pk}

class CreateUserAuthVerifyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerifyEmail
        fields = [
            'email',
        ]

    def create(self, validated_data):
        email, otp_code = [ validated_data['email'], pyotp.TOTP('base32secret3232').now() ]
        
        instance = UserVerifyEmail.objects.create(email=email.lower(), otp_code=otp_code)
        instance.save()
        
        ctx = {
            'message': 'Verification code',
            'message2': 'Use this code to verify your email. You can copy and paste this code.',
            'otp_code': otp_code,
            'logo': os.getenv('EMAIL_LOGO')
        }

        self.send_mail(email, ctx)
        return {'pk': instance.pk, "email": instance.email}
    
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