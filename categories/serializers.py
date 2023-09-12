from rest_framework import serializers
from categories.models import *
from utils.helpers import create_uid
from PIL import Image
import os

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
            'product_specification',
            'products'
        ]

class CategoryProductPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'pk',
            'uid',
            'title',
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

class SubcategoryProductPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = [
            'pk',
            'uid',
            'title'
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