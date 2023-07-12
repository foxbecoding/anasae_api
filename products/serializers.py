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
            'quantity',
            'category',
            'subcategory' 
        ]

class CreateProductSerializer(serializers.ModelSerializer):

    price = serializers.CharField(write_only=True)

    class Meta:
        model = Product
        fields = [
            'brand',
            'category',
            'subcategory' ,
            'title',
            'description',
            'sku',
            'isbn',
            'quantity',
            'price'
        ]

    def validate(self, attrs):
        Product_Instance = Product.objects.create(
            uid = create_uid('pro-'),
            brand = attrs.get('brand'),
            category = attrs.get('category'),
            subcategory = attrs.get('subcategory'),
            title = attrs.get('title'),
            description = attrs.get('description'),
            quantity = attrs.get('quantity'),
            sku = attrs.get('sku'),
            isbn = attrs.get('isbn')
        )

        Product_Instance.save()
        stripe.Product.create(
            name=Product_Instance.title,
            metadata={ 'pk': Product_Instance.id }
        )
        return attrs