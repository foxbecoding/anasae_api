from rest_framework import serializers
from products.models import *
from utils.helpers import create_uid
from PIL import Image
import stripe, requests, os, calendar, time

env = os.getenv

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'pk',
            'uid',
            'title',
            'description',
            'sku',
            'isbn',
            'description',
            'quantity',
            'category',
            'subcategory' 
        ]

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'brand',
            'category',
            'subcategory' 
        ]

    def validate(self, attrs):
        
        return attrs