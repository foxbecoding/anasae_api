from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import *
from utils.helpers import create_uid
import stripe, os, re

env = os.getenv

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'uid',
            'first_name',
            'last_name',
            'email',
            'username',
            'display_name',
            'date_of_birth',
            'agreed_to_toa',
            'is_active',
            'stripe_customer_id',
            'addresses',
            'logins',
            'gender_choice',
            'image',
            'payment_methods',
            'owned_brands',
            'followers',
            'followed_users'
        ]

class EditUserSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'display_name',
            'username',
            'password',
            'confirm_password'
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        attrs['password_changed'] = False
        is_password_change = 'password' in attrs or 'confirm_password' in attrs
        both_passwords_exists = 'password' in attrs and 'confirm_password' in attrs
        
        if attrs.get('username') and not re.match("^[A-Za-z0-9_-]*$", attrs.get('username')):
            msg = 'Only letters, numbers and underscores are allowed'
            raise serializers.ValidationError({"username": msg}, code='authorization')

        if is_password_change:
            if not both_passwords_exists:
                msg = 'Passwords must match.'
                raise serializers.ValidationError({'errors': msg}, code='authorization')
            
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            if password != confirm_password:
                msg = 'Passwords must match.'
                raise serializers.ValidationError({'errors': msg}, code='authorization')
            
            User_Instance = User.objects.get(pk=str(self.context['request'].user.id))
            User_Instance.password=make_password(password)
            User_Instance.save()
            attrs['password_changed'] = True
        
        return attrs

class CreateUserSerializer(serializers.ModelSerializer):
    
    # Create hidden password field for password confirmation
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    gender = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'confirm_password',
            'date_of_birth',
            'gender'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
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

        # Check if passwords matches
        if password != confirm_password:
            msg = 'Passwords must match.'
            raise serializers.ValidationError({"password": msg}, code='authorization')
        
        uid = create_uid('u-')
        stripe_customer = stripe.Customer.create(
            email = attrs.get('email').lower(),
            name = attrs.get('first_name')+' '+attrs.get('last_name'),
            metadata = {
                "uid": uid
            }                
        )
        stripe_customer_id = stripe_customer.id

        # Save User in database
        User_Instance = User.objects.create(
            uid = uid,
            first_name = attrs.get('first_name'),
            last_name = attrs.get('last_name'),
            email = attrs.get('email').lower(),
            username = attrs.get('username').lower(),
            password = make_password(attrs.get('password')),
            agreed_to_toa = True, 
            date_of_birth = attrs.get('date_of_birth'), 
            stripe_customer_id = stripe_customer_id
        )
        User_Instance.save()

        gender_pk = attrs.get('gender')
        User_Gender_Instance = UserGender.objects.get(pk=gender_pk)
        User_Gender_Choice_Instance = UserGenderChoice.objects.create(
            user_gender = User_Gender_Instance,
            user = User_Instance
        )
        User_Gender_Choice_Instance.save()

        attrs['user'] = User_Instance
        return attrs  