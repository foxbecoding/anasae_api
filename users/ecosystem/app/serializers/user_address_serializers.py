from rest_framework import serializers
from users.models import *
import os

env = os.getenv

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            'pk',
            'full_name',
            'phone_number',
            'street_address',
            'street_address_ext',
            'country',
            'state',
            'city',
            'postal_code',
            'is_default'
        ]

class CreateUserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            'user',
            'full_name',
            'phone_number',
            'street_address',
            'street_address_ext',
            'country',
            'state',
            'city',
            'postal_code'
        ]

class EditUserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            'full_name',
            'phone_number',
            'street_address',
            'street_address_ext',
            'country',
            'state',
            'city',
            'postal_code',
            'is_default'
        ]