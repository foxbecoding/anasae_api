from rest_framework import serializers
from cart.models import *

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'pk',
            'uid',
            'user',
            'items'
        ]

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'pk',
            'cart',
            'item'
        ]