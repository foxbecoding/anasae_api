from rest_framework import serializers
from products.models import ProductListing
import os
from pprint import pprint

env = os.getenv

class ProductListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductListing
        fields = [
            'pk',
            'uid',
            'title',
            'image',
            'products',
            'brand',
            'base_variant',
            'category',
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

class ProductListingPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductListing
        fields = [
            'pk',
            'uid',
            'title',
            'image',
            'products',
            'brand',
            'base_variant',
            'category'
        ]