from rest_framework import serializers
from users.models import *
import os


env = os.getenv

class UserPaymentMethodBillingAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserPaymentMethodBillingAddress
        fields = [
            'pk',
            'user',
            'payment_method',
            'address'
        ]

class CreateUserPaymentMethodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserPaymentMethodBillingAddress
        fields = [
            'user',
            'payment_method',
            'address'
        ]