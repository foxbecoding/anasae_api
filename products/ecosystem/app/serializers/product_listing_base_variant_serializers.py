from rest_framework import serializers
from products.models import ProductListingBaseVariant
import os
from pprint import pprint

env = os.getenv

class ProductListingBaseVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductListingBaseVariant
        fields = [
            'pk',
            'product',
            'product_listing',
        ]

class EditProductListingBaseVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductListingBaseVariant
        fields = [
            'product'
        ]