from rest_framework import serializers
from products.models import ProductListing
import stripe, os

env = os.getenv

class ProductListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductListing
        fields = [
            'pk',
            'uid',
            'title',
            'brand',
            'products',
            'created',
            'updated'
        ]