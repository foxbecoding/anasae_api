from rest_framework import serializers
from users.models import *
import os


env = os.getenv

class UserPaymentMethodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserPaymentMethod
        fields = [
            'pk',
            'stripe_pm_id'
        ]

class CreateUserPaymentMethodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserPaymentMethod
        fields = [
            'user',
            'stripe_pm_id'
        ]