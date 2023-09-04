from rest_framework import serializers
from users.models import *
import os


env = os.getenv

class UserBillingAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserBillingAddress
        fields = [
            'pk',
            'user',
            'payment_method',
            'address'
        ]

class CreateUserBillingAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserBillingAddress
        fields = [
            'user',
            'payment_method',
            'address'
        ]