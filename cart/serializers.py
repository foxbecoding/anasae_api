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
            'item',
            'quantity'
        ]

class CreateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'cart',
            'item',
            'quantity'
        ]

class EditCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'quantity'
        ]