from rest_framework import serializers
from categories.models import *
from utils.helpers import create_uid
from PIL import Image
import stripe, requests, os, calendar, time

env = os.getenv

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'pk',
            'uid',
            'title',
            'description',
            'subcategories',
            'product_specification'
        ]

class CategoryProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProductSpecification
        fields = [
            'pk',
            'items'
        ]

class CategoryProductSpecificationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProductSpecificationItem
        fields = [
            'pk',
            'item',
            'is_required'
        ]

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = [
            'pk',
            'uid',
            'title',
            'description',
            'product_specification'
        ]

class SubcategoryProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubcategoryProductSpecification
        fields = [
            'pk',
            'items'
        ]

class SubcategoryProductSpecificationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubcategoryProductSpecificationItem
        fields = [
            'pk',
            'item',
            'is_required'
        ]