from rest_framework import serializers
from products.models import ProductListing
import os

env = os.getenv

class ProductListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductListing
        fields = [
            'pk',
            'uid',
            'title',
            'brand',
            'image',
            'products',
            'created',
            'updated'
        ]

class EditProductListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductListing
        fields = [
            'image',
            'title',
        ]